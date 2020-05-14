from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from hypothesis.strategies import integers, dictionaries, text, one_of, lists, floats, booleans, characters, binary, none
from hypothesis import given, settings, event, HealthCheck
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition, initialize, invariant
import random
import csv

doc_generator = dictionaries(
        keys=one_of(integers(), text(), characters()),
        values=one_of(
            integers(),
            text(alphabet=one_of(characters(whitelist_categories=('Lo', 'Pf')),
                                                characters(whitelist_categories=('P')),
                                                characters(whitelist_categories=('S', 'Z')),
                                                characters(whitelist_categories=('Z')),
                                                characters(whitelist_categories=('Lt', 'Cf', 'Cc', 'Co')))),
            text(), 
            floats(),
            binary(),
            none(),
            lists(elements=one_of(text(), integers()), min_size=2), 
            booleans(),
            dictionaries(integers(), text())
            ),
        min_size=1
        )
file = open('list_lengths.csv', 'w', newline='\n')
writer = csv.writer(file)
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

    @rule(v=doc_generator)
    def insert_value(self, v):
        d_id = self.database.insert(v)  # TinyDB calculates ID when inserting
        #d_id = 6 # Use this line to test fault injecton
        self.model[d_id] = v # You can also outcomment this, it will find a small falsifying example
        self.ids.append(d_id)

    @rule(v=lists(elements=doc_generator, min_size=2, max_size=1000))
    def insert_values(self, v):
        #event('length:' + str(len(v)))
        writer.writerow(str(len(v)))
        d_ids = self.database.insert_multiple(v)
        i = 0
        for d_id in d_ids:
            self.ids.append(d_id)
            self.model[d_id] = v[i]
            i += 1

    @precondition(lambda self: len(self.ids) > 0)
    @rule()
    def remove(self):
        id_to_remove = self.ids.pop(0)
        self.model.pop(id_to_remove)
        self.database.remove(doc_ids=[id_to_remove])

    @rule()
    def remove_all(self):
        self.database.purge_tables()
        self.model.clear()
        self.ids.clear()

    @precondition(lambda self: len(self.ids) > 0)
    @invariant()
    def get_all(self):
        '''Property'''
        assert len(self.model) == len(self.database.all())

    @precondition(lambda self: len(self.ids) > 0)
    @invariant()
    def contains_agree(self):
        '''Property'''
        some_id = random.choice(self.ids)
        assert (some_id in self.model) == (self.database.contains(doc_ids=[some_id]))

    @precondition(lambda self: len(self.ids) > 0)
    @invariant()
    def values_agree(self):
        '''Property'''
        some_id = random.choice(self.ids)
        assert self.database.get(doc_id=some_id) == self.model[some_id]

# Adjust any settings here, default max is 100 examples, 50 is default step count
TinyDBComparison.TestCase.settings = settings(
    max_examples=200, stateful_step_count=100, suppress_health_check=[HealthCheck.data_too_large]
)

TestDBComparison = TinyDBComparison.TestCase