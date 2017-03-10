import json
from collections import OrderedDict
import os
from app import app
from app.utils.logger import logger

DB_INDEX_FILENAME = 'db_index_min.json'

template_dir = app.config['TEMPLATEDIR']
json_dir = os.path.join(template_dir, 'json')

db_path = os.path.join(json_dir, DB_INDEX_FILENAME)
with open(db_path) as fp:
    db_json = json.load(fp)
    # TODO: Stor Pre-sorted DB?

logger.info('DB_INDEX.JSON loaded.')

available_apis = app.config['AVAILABLE_APIS']
namespace_jsons = {}

# REMOVED: SAVED ON S3 requested directly through AJAX
# for year in available_apis:
#     filename = 'namespace_{year}_min.json'.format(year=year)
#     fullpath = os.path.join(json_dir, filename)
#     with open(fullpath) as fp:
#         jdata = json.load(fp, object_hook=OrderedDict)
#     namespace_jsons[year] = jdata
# logger.info('Namespace Tree loaded.')
