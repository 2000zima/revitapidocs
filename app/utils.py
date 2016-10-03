import os
import time
from bs4 import BeautifulSoup
from itertools import permutations
import ujson

from app import app, cache
from app.logger import logger

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
def get_schema(*path):
    """This should be stored/cached in database"""
    template_dir = app.config['TEMPLATEDIR']
    filepath = '/'.join(path)
    fullpath = '{}/{}'.format(template_dir, filepath)
    logger.debug('*** Getting schema for : %s', fullpath)
    try:
        with open(fullpath) as fp:
            soup = BeautifulSoup(fp.read(), 'html.parser')
    except IOError as errmsg:
        logger.error(errmsg)
    else:
        try:
            name = soup.title.string.strip()
            description = soup.find(id='mainBody').find('div').text.strip()
            # description = soup.find(id='mainBody').find('div', { "class": "summary"}).text.strip()
            # Pages that have no summary description return symbol "A"
            # If description is too short (< 3), name is used instead
            if len(description) < 3 or len(description) > 300:
                description = 'Documentation of {}'.format(name)
            namespace = soup.find(id='mainBody').find('a').text.strip()
        except AttributeError as errmsg:
            logger.error(errmsg)
        else:
            return {'name': name,
                    'description': description,
                    'namespace': namespace}
    logger.error('Failed to get schema:: %s', fullpath)
    return

@cache.cached(timeout=86400)
def get_index_json():
    cwd = app.config['BASEDIR']
    fullpath = 'parser/ns_index3.json'
    with open(fullpath) as fp:
        members = ujson.load(fp)
        # members = json.load(fp, object_pairs_hook=OrderedDict)
    return members

def create_permutation_query(query):
    # filename = 'members_{year}.json'.format(year=year)
    # fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder, 'json', filename)
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
