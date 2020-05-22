from tinydb import TinyDB
from tinydb.storages import MemoryStorage, JSONStorage

from hypothesis.strategies import text, integers, binary, lists, dictionaries, characters, one_of, composite, none, floats, booleans
from hypothesis import given, find, settings, Verbosity

db = TinyDB(storage=MemoryStorage)

@composite
def mappings(draw, elem1=integers(), elem2=text()):

    keys = draw(elem1)
    values = draw(elem2)

    return {
        keys : values
    }

''''''

@given(dictionaries(one_of(integers(), text(), characters()), 
                    one_of(text(alphabet=one_of(characters(whitelist_categories=('Lo', 'Pf')),
                                                characters(whitelist_categories=('P')),
                                                characters(whitelist_categories=('S', 'Z')),
                                                characters(whitelist_categories=('Z')),
                                                characters(whitelist_categories=('Lt', 'Cf', 'Cc')))),
                    text(),
                    floats(),
                    integers(),
                    binary(),
                    none(),
                    lists(elements=one_of(text(), integers()), min_size=2),
                    booleans(),
                    dictionaries(integers(), text()),
                    ), min_size=1))
def test_roundtrip(thing):
    db.purge()
    db.insert(thing)
    assert(len(db.all()) == 1)

    #print(thing)

    after_db = db.all()
    assert after_db.pop() == thing

'''@given(dictionaries(one_of(text(), characters()), 
                    one_of(text(alphabet=one_of(characters(whitelist_categories=('Lo', 'Pf')),
                                                characters(whitelist_categories=('P')),
                                                characters(whitelist_categories=('S', 'Z')),
                                                characters(whitelist_categories=('Z')),
                                                characters(whitelist_categories=('Lt', 'Cf', 'Cc')))),
                    text(),
                    floats(),
                    integers(),
                    none(),
                    #binary(),
                    lists(elements=one_of(text(), integers()), min_size=2),
                    booleans(),
                    dictionaries(text(), text()),
                    ), min_size=1))
def test_storage_readwrite(thing):
    storage = JSONStorage('./readwrite.json')

    storage.write(thing)

    assert thing == storage.read()
    storage.close()'''


@given(dictionaries(one_of(text(), characters()), 
                    one_of(text(alphabet=one_of(characters(whitelist_categories=('Lo', 'Pf')),
                                                characters(whitelist_categories=('P')),
                                                characters(whitelist_categories=('S', 'Z')),
                                                characters(whitelist_categories=('Z')),
                                                characters(whitelist_categories=('Lt', 'Cf', 'Cc')))),
                    text(),
                    floats(allow_nan=False),
                    integers(),
                    none(),
                    lists(elements=one_of(text(), integers()), min_size=2),
                    booleans(),
                    dictionaries(text(), text()),
                    ), min_size=1))
def test_no_error_json_storage(thing):
    storage = JSONStorage('./noerrors.json')

    storage.write(thing)

    assert thing == storage.read()
    storage.close()