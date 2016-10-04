import json
import os
from app import app
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)

template_dir = app.config['TEMPLATEDIR']
db_path = os.path.join(template_dir, 'json', 'db_index.json')
with open(db_path) as fp:
    jdata = json.load(fp)

db.insert_multiple(jdata.values())
db_query = Query()

# results = db.search(Page.namespace.search('Autodesk'))
# results = db.search(Page.namespace == 'Autodesk')
