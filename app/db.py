import json
import ujson
import os
import time
from flask import jsonify
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
    Q = Query()
    app.config['TESTING'] = True
    test_app = app.test_client()
    with app.test_request_context('/?name=Peter'):
        app.config['TESTING'] = True
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        for i in range(0,10):
            db.clear_cache()
            t1 = time.time()
            r = db.search(Q.title.search('(add).*(wall)'))
            # sorted_results = sorted(r, key=lambda k: k['title'])
            # jsonify(r)
            print('Done: ', str(time.time()-t1))
