import os
import time
import re
from bs4 import BeautifulSoup
from itertools import permutations
import json

from app import app, cache
from app.logger import logger
from app.db import db_json  # db, db_query

AVAILABLE_APIS = ['2015', '2016', '2017']


@cache.memoize(timeout=86400)
def check_available_years(filename):
    available_in = []
    for year in AVAILABLE_APIS:
        template_dir = app.config['TEMPLATEDIR']
        fullpath = '{}/{}/{}'.format(template_dir, year, filename)
        if os.path.exists(fullpath):
            available_in.append(year)
    return available_in


@cache.memoize(timeout=86400)
def get_schema(filename, year=None):
    """This should be stored/cached in database"""
    results = search_db(filename, 'href')
    if not results:
        return
    entry = results[0]
    if year is None or year in entry.get('year'):
        return entry
    logger.error('Failed to get schema:: %s', filename)
    return None


def process_query(query):
    # escape brackets/parentesis and other symbols
    query = re.sub(r'\\|;|\(|\)|\[|\]', '.', query)
    # Make Space Optional
    query = re.sub(r'\s', r'.*', query)
    return query
    # Old Permutation
    # split_query = query.split(' ')
    # if len(split_query) > 2:
    #     logger.debug('Too Many words for permutation search using simple query.')
    #     return '.'.join(split_query)
    #
    # perm_query = permutations(split_query)
    # final_query = ''
    # for combo in perm_query:
    #     combo = '.*'.join('({})'.format(x) for x in combo)
    #     final_query += '({})|'.format(combo)
    # query = final_query[0:-1]



class Timer(object):
    "Time and TimeIt Decorator"
    def __init__(self):
        self.start_time = time.time()

    def stop(self):
        end_time = time.time()
        duration = end_time - self.start_time
        return duration

    @staticmethod
    def time_function(name):
        def wrapper(func):
            def wrap(*ags, **kwargs):
                logger.debug('START: {}'.format(name))
                t = Timer()
                rv = func(*ags, **kwargs)
                duration = t.stop()
                logger.debug('Done: {} sec'.format(duration))
                return rv
            return wrap
        return wrapper


@Timer.time_function('SEARCH DB')
def search_db(pattern=None, field=None):
    try:
        results = [member for member in db_json.values() if
                   re.search(pattern, member.get(field))]
    except Exception as errmsg:
        logger.error('search_db query error: {}|{}'.format(pattern, field))
        return []
    else:
        return results
