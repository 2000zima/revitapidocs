import json
import os

from tinydb import TinyDB, where, Query
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)

with open(r'parser/ns_index2.json') as fp:
    jdata = json.load(fp)

db.insert_multiple(jdata)
Page = Query()
# r = db.search(Page.namespace.search('Autodesk'))
