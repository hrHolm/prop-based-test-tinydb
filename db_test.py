from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers
from hypothesis import given, settings


@given(integers(), integers())
def insertTwo(int, int2):
    db.purge()
    db.insert({'int': int, 'char': 'a'})
    db.insert({'int': int2, 'char': 'b'})
    assert len(db.all()) == 2

def test_db_insert2():
    assert len(db.all()) == 2


if __name__ == "__main__":
    db = TinyDB(storage=MemoryStorage)
    insertTwo()
    print(db.all())


