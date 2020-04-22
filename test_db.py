from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers
from hypothesis import given, settings

db = TinyDB(storage=MemoryStorage)

@given(integers(), integers())
def test_insert_two(x, y):
    db.purge()
    db.insert({'int': x, 'char': 'a'})
    db.insert({'int': y, 'char': 'b'})
    assert len(db.all()) == 2