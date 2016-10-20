import json
import os
from app import app
from app.logger import logger

template_dir = app.config['TEMPLATEDIR']
json_dir = os.path.join(template_dir, 'json')

# LOAD_DB Index
db_path = os.path.join(json_dir, 'db_index.json')
with open(db_path) as fp:
    db_json = json.load(fp)
logger.info('DB_INDEX.JSON loaded.')


available_apis = app.config['AVAILABLE_APIS']
namespace_jsons = {}

for year in available_apis:
    filename = 'ns_{year}.json'.format(year=year)
    fullpath = os.path.join(json_dir, filename)
    with open(fullpath) as fp:
        jdata = json.load(fp)
    namespace_jsons[year] = jdata

logger.info('Namespace Tree loaded.')
