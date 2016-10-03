import json
import os

from app import app
from tinydb import TinyDB, where, Query
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

if __name__ == '__main__':
    q = '9a5b0b20-5f31-9af9-78a1-a518ef92610c.htm'
    Q = Query()
    r = db.search(Q.href=='9a5b0b20-5f31-9af9-78a1-a518ef92610c.htm')
    print(r)
    print(r[0]['year'])
