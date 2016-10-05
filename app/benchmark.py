import json
import os
import re
from app.db import db, db_query, jdata, where
from app.utils import Timer


@Timer.time_function('TINY---------')
def bench_tiny(pat):
    "Average: 0.25"
    results = db.search(db_query.title.search(pat))
    return results


@Timer.time_function('TINY WHERE---------')
def bench_tiny_func(pat):
    "Average: 0.20"
    # test_func = lambda s: re.search(pat, s)
    results = db.search(db_query.title.test(lambda s: re.search(pat, s)))
    return results


@Timer.time_function('ITER----------')
def bench_iter_re(query):
    "Average: 0.5-0.8"
    return [d for k, d in jdata.items() if re.search(pat, d['title']) is not None]
    # print(type(jdata.keys()))


pat = re.compile(r'((add).*(wall))|(tag).*(property)', re.IGNORECASE)
r1 = bench_tiny(pat)
r2 = bench_tiny_func(pat)
r3 = bench_iter_re(bench_iter_re)

print(len(r1))
print(len(r2))
print(len(r3))
# bench_tiny('((add).*(wall))|(tag).*(property)')
