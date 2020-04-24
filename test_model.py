from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers, dictionaries, text, one_of
from hypothesis import given, settings, event
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, precondition
from collections import defaultdict


class TinyDBComparison(RuleBasedStateMachine):
    '''
    TODO: make one without bundles since: "Note that currently preconditions can’t access 
    bundles; if you need to use preconditions, you should store relevant data on the instance instead."
    '''

    def __init__(self):
        super(TinyDBComparison, self).__init__()
        self.database = TinyDB(storage=MemoryStorage)  # sut, memory db makes sure states are reset
        self.model = defaultdict(set)

    ids = Bundle("ids")
    documents = Bundle("documents")


    @rule(target=documents, v=dictionaries(keys=integers(min_value=0), values=integers(min_value=0)))
    def add_value(self, v):
        '''Generate value to insert'''
        return v

    @rule(target=ids, k=ids, v=documents) # TODO: removing k from here results in "TypeError: unhashable type: 'dict'"
    def insert_value(self, v):
        d_id = self.database.insert(v)  # TinyDB calculates ID when inserting
        print(d_id, v)
        d_id = 6 # TODO: injected fault is not picked up...
        self.model[d_id].add(v)
        return d_id


    @rule(k=ids)
    def remove(self, k):
        self.model.pop(k)
        self.database.remove(doc_id=k)

   
    @rule()
    def get_all(self):
        assert len(self.model) == len(self.database.all())

    
    @rule(k=ids)
    def contains_agree(self, k):
        '''Property'''
        assert (self.model[k] is not None) and (self.database.contains(doc_ids=[k]) is not False)

    @rule(k=ids)
    def values_agree(self, k):
        '''Property'''
        assert set(self.database.get(doc_ids=[k])) == self.model[k]


TestDBComparison = TinyDBComparison.TestCase
