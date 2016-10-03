import os
import time
from bs4 import BeautifulSoup
from itertools import permutations
import json

from app import app, cache
from app.logger import logger
from app.db import db, db_query

AVAILABLE_APIS = ['2015', '2016', '2017']


# @cache.cached(timeout=86400)
def check_available_years(filename):
    available_in = []
    for year in AVAILABLE_APIS:
        template_dir = app.config['TEMPLATEDIR']
        fullpath = '{}/{}/{}'.format(template_dir, year, filename)
        if os.path.exists(fullpath):
            available_in.append(year)
    return available_in


# @cache.cached(timeout=86400)
def get_schema(filename, year=None):
    """This should be stored/cached in database"""
    results = db.search(db_query.href == filename)
    if not results:
        return
    entry = results[0]
    if year is None or year in entry.get('year'):
        return entry
    logger.error('Failed to get schema:: %s', filename)
    return None


def create_permutation_query(query):
    # query = 'Create Wall Method'
    split_query = query.lower().split(' ')
    # query = ['create', 'wall', 'method']
    perm_query = permutations(split_query)
    # (('create', 'wall', 'method'), ('wall', 'create')

    final_query = ''
    for combo in perm_query:
        combo = '.+'.join('({})'.format(x) for x in combo)
        final_query += '({})|'.format(combo)
    query = final_query[0:-1]
    return query

class Timer(object):
    "Simple Timer."
    def __init__(self):
        self.start_time = time.time()

    def stop(self):
        end_time = time.time()
        duration = end_time - self.start_time
        return duration
