from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

'''
This file is just for trying out the different API methods
'''

db = TinyDB(storage=MemoryStorage)
#User = Query()
d_id = db.insert({123: 'John', 'age': 22})
print(d_id)
#db.search(User.name == 'John')
#[{'name': 'John', 'age': 22}]
print(db.contains(doc_ids=[1]))