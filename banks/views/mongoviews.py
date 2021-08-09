from flask import Flask, redirect, abort, request
from flask_restful import Resource, Api
from bson.objectid import ObjectId

from banks.models.models import MongoDatabaseModel
from banks.models.sample_banks import MONGO_SAMPLE_BANKS

def init_app(app: Flask) -> None:
    api = Api(app)
    database = MongoDatabaseModel()

    class MongoAddSampleBanks(Resource):
        def get(self):
            if not len(database.get_by_query()) > 0:
                database.insert_many(MONGO_SAMPLE_BANKS)
            return redirect('/mongo/banks/', 308)
    
    class MongoListAndCreateBanks(Resource):
        def get(self):
            banks, status_code = [], 200
            for document in database.get_by_query():
                bank = {}
                for k, v in document.items():
                    if not isinstance(v, ObjectId):
                        bank[k] = v
                banks.append(bank)
            if not banks:
                return redirect('/mongo/', 303)
            return banks, status_code

        def post(self):
            try:
                assert_message = 'Document must have {}'
                bank, status_code = request.json, 323
                assert isinstance(bank, dict), assert_message.format('only one')
                assert 'bank' in bank.keys(), assert_message.format('bank')
                assert 'pop_name' in bank.keys(), assert_message.format('pop_name')
                assert 'cod' in bank.keys(), assert_message.format('cod')
                assert 'infos' in bank.keys(), assert_message.format('infos')
                assert 'is_digital' in bank['infos'].keys(), assert_message.format('infos.is_digital')
                assert 'website' in bank['infos'].keys(), assert_message.format('infos.website')
                database.insert(bank)
                return redirect(f'/mongo/{bank["cod"]}/', status_code)
            except AssertionError as error:
                status_code = 400
                bank = {
                    'message': str(error),
                    'status_code': status_code
                }
            except Exception:
                abort(500)
            return bank, status_code

    class MongoBankByCod(Resource):
        def get(self, bank_cod):
            try:
                status_code = 200
                bank = database.get_by_query(
                    {"cod": bank_cod}
                )[0]
                bank['_id'] = f'ObjectId({str(bank["_id"])})'
            except IndexError:
                abort(404)
            except Exception:
                abort(500)
            return bank, status_code
        
        def put(self, bank_cod):
            try:
                update_assert_message = 'An error happened updating {}'
                bank, status_code, update_which = request.json, 201, {'cod': bank_cod}
                assert isinstance(bank, dict), 'Just updated one document'
                assert 'bank' not in bank.keys(), 'Field bank cannot be changed'
                assert 'cod' not in bank.keys(), 'Field cod cannot be changed'

                if pop_name := bank.get('pop_name'):
                    assert isinstance(pop_name, str), 'pop_name must be string'
                    assert database.update(
                        update_which, {'$set': {'pop_name': pop_name}}
                    ), update_assert_message.format('pop_name')
                
                if infos := bank.get('infos'):
                    if is_digital := infos.get('is_digital'):
                        assert isinstance(is_digital, bool), 'is_digital must be boolean'
                        assert database.update(
                            update_which, {'$set': {'infos.is_digital': is_digital}}
                        ), update_assert_message.format('is_digital')

                    if website := infos.get('website'):
                        assert isinstance(website, str), 'website must be string'
                        assert database.update(
                            update_which, {'$set': {'infos.website': website}}
                        ), update_assert_message.format('website')

                    if hip := infos.get('has_investment_platform'):
                        assert isinstance(hip, bool), f'{hip} must be boolean'
                        assert database.update(
                            update_which, {'$set': {'infos.has_investment_platform': hip}}
                        ), update_assert_message.format(f'{hip}')
                return redirect(f'/mongo/{bank_cod}/')
            except AssertionError as error:
                status_code = 400
                bank = {
                    'message': str(error),
                    'status_code': status_code
                }
            except Exception as error:
                print(error)
                abort(500)
            return bank, status_code
        
        def delete(self, bank_cod):
            try:
                assert database.delete({"cod": bank_cod}), ''
                return redirect('/mongo/banks/')
            except AssertionError:
                abort(404)
            except Exception:
                abort(500)
    
    api.add_resource(MongoAddSampleBanks, '/mongo/')
    api.add_resource(MongoListAndCreateBanks, '/mongo/banks/')
    api.add_resource(MongoBankByCod, '/mongo/<int:bank_cod>/')
