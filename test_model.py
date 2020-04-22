from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers, dictionaries, text
from hypothesis import given, settings, event
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, precondition
from collections import defaultdict


class TinyDBComparison(RuleBasedStateMachine):
    def __init__(self):
        super(TinyDBComparison, self).__init__()
        self.database = TinyDB(storage=MemoryStorage)  # sut
        self.model = defaultdict(set)

    ids = Bundle("ids")
    documents = Bundle("documents")

    '''
    @rule(target=ids, k=st.binary())
    def add_key(self, k):
        return k
    '''

    @rule(target=documents, v=dictionaries(keys=text(), values=integers()))
    def add_value(self, v):
        return v

    @rule(k=ids, v=documents)
    def insert(self, v):
        d_id = self.database.insert(v)  # TinyDB calculates ID when inserting
        self.model[d_id].add(v)

    @precondition(lambda self: len(self.model) > 0)  # TODO: find better precondition
    @rule(k=ids, v=documents)
    def remove(self, k, v):
        self.model[k].discard(v)
        self.database.remove(doc_id=k)

    @precondition(lambda self: len(self.model) > 0)  # TODO: find better precondition
    @rule()
    def get_all(self):
        assert len(self.model) == len(self.database.all())

    @precondition(lambda self: len(self.model) > 0)  # TODO: find better precondition
    @rule(k=ids)
    def search_id(self, k):
        assert self.model[k] == self.database.search(id == k)

    @rule(k=ids)
    def values_agree(self, k):
        '''Property'''
        assert set(self.database.get(doc_id=k)) == self.model[k]


TestDBComparison = TinyDBComparison.TestCase
