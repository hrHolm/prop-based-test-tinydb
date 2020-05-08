from tinydb import TinyDB
from tinydb.storages import MemoryStorage, JSONStorage

from hypothesis.strategies import text, integers, binary, lists, dictionaries, characters, one_of, composite
from hypothesis import given

db = TinyDB('./db.json', storage = JSONStorage)

@composite
def mappings(draw, elem1=integers(), elem2=text()):

    keys = draw(elem1)
    values = draw(elem2)

    return {
        keys : values
    }

@given(one_of(mappings(integers(), text()),
            mappings(text(), text()),
            mappings(integers(), integers()),
            mappings(characters(), text()),
            mappings(text(), lists(integers())),
            mappings(integers(), binary()),
            mappings(integers(), dictionaries(integers(), text()))))
def test_roundtrip(thing):
    db.purge()
    db.insert(thing)
    assert(len(db.all()) == 1)

    after_db = db.all()
    assert after_db.pop() == thing

@given(one_of(mappings(integers(), text()),
            mappings(text(), text()),
            mappings(integers(), integers()),
            mappings(characters(), text()),
            mappings(text(), lists(integers())),
            mappings(integers(), binary()),
            mappings(integers(), dictionaries(integers(), text()))))
def test_storage_readwrite(thing):
    storage = JSONStorage('./readwrite.json')

    storage.write(thing)

    assert thing == storage.read()
    storage.close()