import os
import time
import re
from bs4 import BeautifulSoup
from itertools import permutations
import json
import requests

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


# @cache.memoize(timeout=86400)
def get_schema(filename, year=None):
    """This should be stored/cached in database"""
    logger.debug('Getting Schema: {}|{}'.format(filename, year))
    
    results = search_db(filename, 'href')
    if not results:
        return
    # Gives preference to 'entries that are namespace'
    for entry in results:
        if entry['type'] == 'namespace':
            break
    if year is None or year in entry.get('year'):
        logger.debug(entry)
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

def track_search(query, num_results=None, clicked=None):
    ''' Makes put requests to constructo io's api
    to track usage/behavior. Data comes from a special Tracking url
    called by the browser.
    '''
    key = app.config['CONSTRUCTOR_IO_AUTOCOMPLETE_KEY']
    api_key = app.config['CONSTRUCTOR_IO_API_TOKEN']
    auth = (api_key, '')

    headers = {"Content-Type": "application/json"}


    url = "https://ac.cnstrc.com/v1/search?1&autocomplete_key={key}".format(key=key)
    url_click = "https://ac.cnstrc.com/v1/click_through?1&autocomplete_key={key}".format(key=key)

    payload       = {'term': query, 'num_results': num_results}
    payload_click = {'term': query,
                    'autocomplete_section': 'Search Suggestions',
                    'item_id': clicked}

    if clicked:
        url = url_click
        payload = payload_click
    else:
        try:
            num_results = int(num_results)
        except:
            logger.debug('Could not convert num_results to in. Will Fail.')
            logger.debug('num_results: {}'.format(num_results))

    response = requests.post(url, headers=headers, auth=auth, json=payload)
    if response.status_code == 204:
        response_json = {'message':'Success', 'payload':payload}
        logger.debug('TRACKED: {}'.format(payload))
    else:
        logger.debug('ERROR Tracking Search')
        response_json = response.json()
        logger.debug('MSG: {}'.format(response_json))

    return response, response_json

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
