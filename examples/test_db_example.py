import shutil
import tempfile
import csv

from collections import defaultdict
import hypothesis.strategies as st
from hypothesis.database import DirectoryBasedExampleDatabase
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, HealthCheck
from hypothesis import settings

file = open('list_lengths.csv', 'w', newline='\n')
writer = csv.writer(file)
class DatabaseComparison(RuleBasedStateMachine):
    def __init__(self):
        super(DatabaseComparison, self).__init__()
        writer.writerow(['init_state'])
        self.tempd = tempfile.mkdtemp()
        self.database = DirectoryBasedExampleDatabase(self.tempd)
        self.model = defaultdict(set)

    keys = Bundle("keys")
    values = Bundle("values")

    @rule(target=keys, k=st.binary())
    def add_key(self, k):
        writer.writerow(['add_key'])
        return k

    @rule(target=values, v=st.binary())
    def add_value(self, v):
        writer.writerow(['add_value'])
        return v

    @rule(k=keys, v=values)
    def save(self, k, v):
        writer.writerow(['save'])
        self.model[k].add(v)
        self.database.save(k, v)

    @rule(k=keys, v=values)
    def delete(self, k, v):
        writer.writerow(['delete'])
        self.model[k].discard(v) # outcomment this to see it working
        self.database.delete(k, v)

    @rule(k=keys)
    def values_agree(self, k):
        assert set(self.database.fetch(k)) == self.model[k]

    def teardown(self):
        writer.writerow(['teardown'])
        shutil.rmtree(self.tempd)

# Adjust any settings here, default max is 100 examples, 50 is default step count
DatabaseComparison.TestCase.settings = settings(
    max_examples=200, stateful_step_count=100, suppress_health_check=[HealthCheck.data_too_large]
)
TestDBComparison = DatabaseComparison.TestCase