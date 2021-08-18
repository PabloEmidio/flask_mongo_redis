from unittest.mock import patch

import pytest
import fakeredis

from .exceptions import DatabaseNotVoid, BadTestPracticeError
from banks.models.models import RedisDatabaseModel

@pytest.fixture
def insert_example():
    return [
        {"cod": "123"},
        {"test": "test"}
    ]

@pytest.fixture
def db(insert_example):
    with patch('banks.models.models.redis.StrictRedis', new=fakeredis.FakeStrictRedis):
        db = RedisDatabaseModel()
        if not len(db.get_values()) == 0:
            raise DatabaseNotVoid()
        yield db
        [db.delete(key) for key in db.get_keys()]


def test_crud_redis(db, insert_example):
    try:
        cod = insert_example[0]['cod']
        bank_key, bank_info = f'banks:{cod}', f'banks:{cod}:infos'
    except KeyError:
        raise BadTestPracticeError()
    except IndexError:
        raise BadTestPracticeError()
    db.insert(insert_example[0], insert_example[1])
    assert len(db.get_keys()) == 2
    assert db.update(bank_key, {'cod': '321'})
    assert db.get_values(bank_key, bank_info)[0]['cod'] == '321'
    assert db.update(bank_info, {'test': 'updated'})
    assert db.get_values(bank_key, bank_info)[1]['test'] == 'updated'
    assert db.delete(bank_key, bank_info)
    assert len(db.get_keys()) == 0
