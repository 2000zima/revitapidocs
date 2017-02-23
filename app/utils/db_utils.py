import os
import time
import re
from bs4 import BeautifulSoup
from itertools import permutations
import json
import requests

from app import app, cache
from app.utils.logger import logger
from app.utils.misc import Timer
from app.utils.db import db_json

AVAILABLE_YEARS = app.config['AVAILABLE_APIS']
API_DOCS_PATH = app.config['API_DOCS_PATH']
API_DOCS_NAME = app.config['API_DOCS_NAME']


# @cache.memoize(timeout=3600)  # 1 Hour
def get_entry(filename):
    entry = search_db(filename, field='href')
    return entry


# @cache.memoize(timeout=3600) # 1 Hour
# def get_file_available_years(filename):
#     ''' Checks which years resource file is available in.
#     Returns: list of years a string, empty string if there not matches
#     '''
#     available_in = []
#     for year in AVAILABLE_YEARS:
#         fullpath = os.path.join(API_DOCS_PATH, year, filename)
#         if os.path.exists(fullpath):
#             available_in.append(year)
#     logger.debug('Available in [{}]:{}'.format(available_in, filename))
#     if not available_in:
#         logger.error('File was not found in any year: {}'.format(filename))
#     import pdb; pdb.set_trace()
#     return available_in


def get_best_entry_match(entry, target_year):
    """Figures out the best match based on the target year.
    The best match is self is content is the first to exists or has been updated
    if That doesn't apply
    For example is the years entry are:
    {'years': {'2015': 'exists',
               '2016': 'unchanged',
               '2017': 'updated',
               '2017.1': 'unchanged'}}

    Target > Best Match:
    - 2015 > 2015
    - 2016 > 2015
    - 2017 > 2017
    - 2017.1 > 2017
    """
    years_dict = entry['years']

    if target_year not in years_dict:
        return None

    if years_dict[target_year] == 'exists' or years_dict[target_year] == 'updated':
        return target_year

    possible_years = [year for year, status in years_dict.items()
                      if year < target_year and
                      ((status == 'exists') or (status == 'updated'))]

    if not possible_years:
        logger.error('Could not Find best match for: {}:{}'.format(entry['href'], target_year))
        raise Exception('Could not find template match f')
    else:
        last_possible_year = sorted(possible_years)[-1]
        return last_possible_year


def process_query(query):
    ''' Cleans up Query string and compiles as re pattern.
    Replaces, slashes, brackets, and others symbols that can break
    the re-pattern. Makes space optional.
    wall class > wall.*class
    wall*class > wall.*class
    /, \ , ( , ), [ , ] etc become .
    '''
    # escape brackets/parentesis and other symbols
    final_query = re.sub(r'\\|;|\(|\)|\[|\]', '.', query)
    # Make Space Optional
    final_query = re.sub(r'\s|\*', r'.*', final_query)
    # logger.debug('process_query in: {}'.format(query))
    # logger.debug('process_query out: {}'.format(final_query))
    return final_query


@Timer.time_function('SEARCH DB')
def search_db(pattern=None, field=None):
    """ Searches db_index.json
    If looking up by href, which is the key, a dictionary look up is used,
    else it uses list comprehensian + regex search
    """
    if field == 'href':
        return db_json.get(pattern)

    try:
        results = [member for member in db_json.values() if
                   re.search(pattern, member.get(field))]
    except Exception as errmsg:
        logger.error('search_db query error: {}|{}'.format(pattern, field))
        return []
    else:
        return results


# @Timer.time_function('Prioritize Results')
def prioritize_match(results=None, raw_query=None, field=None):
    """If Search query matches title exactly (no fuzzy or space forgiveness)
    result is pushed up to top of list
    """
    try:
        pattern = re.compile(raw_query, re.IGNORECASE)
    except Exception as errmsg:
        logger.error('prioritize: Could not compile raw_query: {}'.format(raw_query))
        return results
    prioritized_results = []
    for member in results:
        if re.match(pattern, member.get(field)):
            prioritized_results.insert(0, member)
            logger.debug('Priority Match Found: {}'.format(pattern))
        else:
            prioritized_results.append(member)
    return prioritized_results
