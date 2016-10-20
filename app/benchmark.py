import json
import os
import re
from app.db import db_json
from app.utils import Timer, search_db


@Timer.time_function('TINY---------')
def bench_search(pat, field):
    "Average: 0.08"
    results = search_db(pat, field)
    return results


@Timer.time_function('TINY WHERE---------')
def bench_get(pat, field):
    "Average: 0.03"
    # test_func = lambda s: re.search(pat, s)
    results = search_db(pat, field)
    return results



pat = re.compile(r'((add).*(wall))|(tag).*(property)', re.IGNORECASE)
r1 = bench_search(pat, 'title')

href = '11785869-cc9e-03fc-97db-767a59af10a1.htm'
title = 'Autodesk.Revit.UI.Selection Namespace'
r2 = bench_get(href, 'href')
r3 = bench_get(title, 'title')

print(len(r1))
print(len(r2))
print(len(r3))
# print(len(r3))
# bench_tiny('((add).*(wall))|(tag).*(property)')

results = []

for i in range(50):
    t = Timer()
    # bench_get(pat, 'title')     # 0.88 avg
    # bench_get(title, 'title')   # 0.37
    # bench_get(href, 'href')       # 0.39 - No key
    bench_get(href, 'href')       # 0.0003 - W key
    r = t.stop()
    results.append(r)

avg = sum(results)/len(results)
print('AVG: >>> ' + str(avg))
