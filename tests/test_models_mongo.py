from unittest.mock import patch

import pytest
import mongomock

from .exceptions import CollectionNotVoid, BadTestPracticeError
from banks.models.models import MongoDatabaseModel

@pytest.fixture
def insert_example():
    return {"test": "test"}

@pytest.fixture
def db(insert_example):
    with patch('banks.models.models.pymongo', new=mongomock):
        db = MongoDatabaseModel(collection='tests')
        if not len(db.get_by_query()) == 0:
            raise CollectionNotVoid()
        yield db
        example_key = list(insert_example.keys())[0]
        try:
            [db.delete({document[example_key]: {"$exists": True}}) for document in db.get_by_query()]
        except KeyError:
            raise BadTestPracticeError()


def test_mongo_crud(db, insert_example):
    assert db.insert(insert_example)
    assert len(db.get_by_query()) == 1
    example_key = list(insert_example.keys())[0]
    assert db.update(insert_example, {"$set": {example_key: "updated"}})
    assert len(db.get_by_query({example_key: "updated"})) == 1
    assert db.delete({example_key: 'updated'})
    assert len(db.get_by_query()) == 0
