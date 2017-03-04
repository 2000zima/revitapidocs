import json
import os
import re

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.utils.db import db_json
from app.utils.db_utils import search_db, process_query
from app.utils.misc import Timer


@Timer.time_function('TINY---------')
def bench_search(pat, field):
    "Average: 0.08"
    results = search_db(pat, field)
    return results

href = '11785869-cc9e-03fc-97db-767a59af10a1.htm'
title = 'Autodesk.Revit.UI.Selection Namespace'



results = []

for i in range(50):
    t = Timer()
    bench_search(href, 'href')       # 0.0003 - W key
    r = t.stop()
    results.append(r)

avg = sum(results)/len(results)
print('START HREF BENCHMARK-----------------')
print('AVG: >>> ' + str(avg))
print('END HREF BENCHMARK-----------------')


query = 'wall class'
p_query = process_query(query)
# pat = re.compile(r'((add).*(wall))|(tag).*(property)', re.IGNORECASE)

results = []

for i in range(50):
    t = Timer()
    r1 = bench_search(p_query, 'title')
    r = t.stop()
    results.append(r)

avg = sum(results)/len(results)
print('START TITLE BENCHMARK-----------------')
print('AVG: >>> ' + str(avg))  # 0.039 - wall class
print('END TITLE BENCHMARK-----------------')
