from typing import List

from dotenv import dotenv_values
import pymongo
import redis

config = dotenv_values('.env')

class MongoDatabaseModel:
    LOCALURI = 'mongodb://localhost/admin'

    def __init__(self, db_name: str='testbanks', collection: str='banks'):
        mongo_uri = config.get('mongouri') or self.LOCALURI
        client = pymongo.MongoClient(mongo_uri)
        self.db = client[db_name]
        self.db = self.db[collection]

    def get_by_query(self, query: dict={}):
        return [match for match in self.db.find(query)]


    def insert(self, document: dict={}) -> None:
        inserted = self.db.insert_one(document)
        return len(str(inserted.inserted_id)) > 0


    def insert_many(self, documents: List[dict]):
        inserted = self.db.insert_many(documents)
        return len(inserted.inserted_ids) > 0


    def update(self, update_which: dict={}, update_set: dict={}):
            updated = self.db.update_one(
                update_which, update_set
            )
            return updated.modified_count > 0
 
    def delete(self, delete_which: dict={}):
        deleted = self.db.delete_one(delete_which)
        return deleted.deleted_count > 0

class RedisDatabaseModel:
        LOCALURI = 'localhost'

        def __init__(self):
            redis_uri = config.get('redisuri') or self.LOCALURI
            self.db = redis.StrictRedis(host=redis_uri, port=6379, db=0, charset='UTF-8', decode_responses=True)

        def get_keys(self, match: str='banks:*'):
            keys = self.db.scan(0, match, count=1000)[1]
            keys.sort()
            return keys

        def get_values(self, bank_key: str = '', info_key: str=''):
            try:
                banks = []
                if not bank_key or not info_key:
                    for key in self.get_keys():
                        banks.append(self.db.hgetall(key))
                else:
                    banks.append(self.db.hgetall(bank_key))
                    banks.append(self.db.hgetall(info_key))
                return banks
            except Exception as error:
                print(error)

        def insert(self, bank_fields: dict[str, str], bank_infos: dict[str, str]):
            cod_bank = bank_fields['cod']
            try: 
                assert self.db.hset(f'banks:{cod_bank}', mapping=bank_fields), 'There was an error'
                assert self.db.hset(f'banks:{cod_bank}:infos', mapping=bank_infos), 'There was an error'
            except Exception as error:
                print(error)

        def update(self, hash_name: str = '', bank_fields: dict[str, str]={'key': 'value'}):
            updated = self.db.hset(hash_name, mapping=bank_fields)
            return updated == 0
        
        def delete(self, bank_key: str = '', info_key: str=''):
            deleted = self.db.delete(bank_key, info_key)
            return deleted >= 1
