from tinydb import TinyDB
from tinydb.storages import MemoryStorage

import hypothesis.strategies as st
from hypothesis import given

db = TinyDB(storage=MemoryStorage)

@st.composite
def mappings(draw, elem1=st.integers(), elem2=st.text()):

    keys = draw(elem1)
    values = draw(elem2)

    return {
        keys : values
    }

@given(st.one_of(mappings(st.integers(), st.text()),
            mappings(st.text(), st.text()),
            mappings(st.integers(), st.integers()),
            mappings(st.characters(), st.text()),
            mappings(st.text(), st.lists(st.integers())),
            mappings(st.integers(), st.binary()),
            mappings(st.integers(), st.dictionaries(st.integers(), st.text()))))
def test_roundtrip(thing):
    db.purge()
    db.insert(thing)
    assert(len(db.all()) == 1)

    after_db = db.all()
    print(after_db)
    assert after_db.pop() == thing