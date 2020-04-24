from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers, dictionaries, text, one_of, binary
from hypothesis import given, settings, event
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, precondition, initialize
from collections import defaultdict
import random

DEADLINE_TIME = 1000

class TinyDBComparison(RuleBasedStateMachine):

    def __init__(self):
        super(TinyDBComparison, self).__init__()
          # sut, memory db makes sure states are reset

    model = {}
    ids = []
    documents = []
    database = None


    @initialize()
    def init_state(self):
        '''Start from fresh in each iteration'''
        self.database = TinyDB(storage=MemoryStorage)
        self.ids = []
        self.documents = []
        self.database.purge_tables()
        self.model = {}

    @rule(v=dictionaries(keys=integers(), values=integers(min_value=0), min_size=1)) 
    def insert_value(self, v):
        d_id = self.database.insert(v)  # TinyDB calculates ID when inserting
        #print(d_id, v)
        # d_id = 6 # Use this line to test fault injecton. It works
        self.model[d_id] = v # You can also outcomment this, it will find a small falsifying example
        print(self.model[d_id])
        self.ids.append(d_id)


    @precondition(lambda self: len(self.ids) > 0)
    @rule()
    def remove(self):
        id_to_remove = self.ids.pop(0)
        self.model.pop(id_to_remove)
        self.database.remove(doc_ids=[id_to_remove])

   
    @rule()
    def get_all(self):
        assert len(self.model) == len(self.database.all())

    
    @precondition(lambda self: len(self.ids) > 0)
    @rule()
    def contains_agree(self):
        '''Property'''
        some_id = random.choice(self.ids)
        assert (self.model[some_id] is not None) and (self.database.contains(doc_ids=[some_id]) is not False)

    @precondition(lambda self: len(self.ids) > 0)
    @rule()
    def values_agree(self):
        '''Property'''
        some_id = random.choice(self.ids)
        assert self.database.get(doc_id=some_id) == self.model[some_id]
    '''
    TODO: look into if this is possible after all, I might've missed something - however it caused flaky generations...
    def teardown(self):
        self.ids = []
        self.documents = []
        self.database.purge_tables()
        self.database.close()
        self.model = {}
    '''

TestDBComparison = TinyDBComparison.TestCase
