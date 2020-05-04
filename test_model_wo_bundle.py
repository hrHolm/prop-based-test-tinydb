from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers, dictionaries, text, one_of, binary, lists
from hypothesis import given, settings, event
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, precondition, initialize
from collections import defaultdict
import random

DEADLINE_TIME = 1000


class TinyDBComparison(RuleBasedStateMachine):

    def __init__(self):
        super(TinyDBComparison, self).__init__()
    model = {}
    ids = []
    documents = []
    database = None

    @initialize()
    def init_state(self):
        '''Start from fresh in each iteration'''
        self.database = TinyDB(
            storage=MemoryStorage)  # sut, memory db makes sure states are reset
        self.ids = []
        self.documents = []
        self.database.purge_tables()
        self.model = {}

    @rule(v=dictionaries(
        keys=one_of(integers(), text()),
        values=one_of(integers(), text()),
        min_size=1
        ))
    def insert_value(self, v):
        d_id = self.database.insert(v)  # TinyDB calculates ID when inserting
        #print(d_id, v)
        # d_id = 6 # Use this line to test fault injecton. It works
        self.model[d_id] = v # You can also outcomment this, it will find a small falsifying example
        self.ids.append(d_id)

    @rule(v=one_of(integers(), text()))
    def insert_values(self, v):
        #Not beautiful, but had trouble getting it working by generating dictionaries
        item = {v: v, v: v}
        item2 = {v: v, v: v}
        item3 = {v: v, v: v}
        d_ids = self.database.insert_multiple([item, item2, item3])  # TinyDB calculates ID when inserting
        self.ids.append(d_ids[0])
        self.ids.append(d_ids[1])
        self.ids.append(d_ids[2])
        self.model[d_ids[0]] = item
        self.model[d_ids[1]] = item2
        self.model[d_ids[2]] = item3

    @rule(v=dictionaries(
        keys=one_of(integers(), text()),
        values=one_of(integers(), text()),
        min_size=1
        ))
    def retrieve_value(self, v):
        new_value = self.database.insert(v)
        doc = self.database.get(doc_id=new_value)
        self.ids.append(new_value)
        self.model[new_value] = doc

    #@rule(v=dictionaries(
    #    keys=one_of(integers(), text()),
    #    values=one_of(integers(), text()),
    #    min_size=1
    #), v2=dictionaries(
    #    keys=one_of(integers(), text()),
    #    values=one_of(integers(), text()),
    #    min_size=1
    #))
    #def update_value(self, v, v2):
        #id_to_update = self.database.insert(v)
        #doc_to_update = self.database.get(doc_id=id_to_update)
        #updated_id = doc_to_update.update(v2)
        #updated_id = self.database.update(v2, cond=doc_to_update)
        #updated_id = self.database.update(v2, doc_ids=[id_to_update])
        #self.ids.append(updated_id)

    # self.model[updated_id] = v2
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
        assert (some_id in self.model) == (self.database.contains(doc_ids=[some_id]))

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

# Adjust any settings here, default max is 100 examples, 50 is default step count
TinyDBComparison.TestCase.settings = settings(
    max_examples=200, stateful_step_count=100
)

TestDBComparison = TinyDBComparison.TestCase