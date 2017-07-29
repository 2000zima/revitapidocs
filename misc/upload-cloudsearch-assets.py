""" AWS CloudSearch Uploader """

# import flask_s3
import re
import json
import boto3
from app import app
from app.utils.db_utils import get_best_entry_match

import logging
logger = logging.getLogger('flask_s3')
logger.setLevel(logging.DEBUG)

print('Uploading CloudSearch Bucket...')

client = boto3.client('cloudsearchdomain', 'us-east-1',
                       endpoint_url = "http://doc-revitapidocs-staging-aikyh7yoyt43gf4wv3pemwlq3i.us-east-1.cloudsearch.amazonaws.com"
                       )

filepath = r'chm_parser\data\out_Merged\db_index.json'
with open(filepath) as fp:
    jdata = json.load(fp)

def sanitize_title(title):
    title = ''.join([c for c in title if c.isalnum()])[0:128]
    if re.match(r"[a-zA-Z0-9\-\_\/\#\:\.\;\&\=\?\@\$\+\!\*'\(\)\,\%]+$", title):
        return title
    else:
        print('Title not valid:')
        print(title)
        import pdb; pdb.set_trace()

items = []
unique_names = {}
for n, entry in enumerate(jdata.values()):
    clean_title = sanitize_title(entry['title'])
    item = { "type": "add",
             "id": sanitize_title('_'.join([entry['href'], clean_title])),
             "fields": {
                        # 'namespace': entry['namespace'],
                        'member_of': entry['member_of'],
                        'title': entry['title'],
                        'tag': entry['tag'],
                        'description': entry['description'],
                        # 'url': entry['href'],
                        "year_2015": entry['years'].get('2015', ''),
                        "year_2016": entry['years'].get('2016', ''),
                        "year_2017": entry['years'].get('2017', ''),
                        "year_20171": entry['years'].get('2017.1', ''),
                        "year_2018": entry['years'].get('2018', ''),
                        }
            }
    # item['text'] = url
    items.append(item)

MAX = None

# with open('tests.json', 'w') as fp:
#     json.dump(items[0:MAX], fp)

CHUNK_SIZE = 2000
for i in range(0, len(items), CHUNK_SIZE):
    print('Uploading Chunk: {}'.format(i))
    items_chunk = items[i: i + CHUNK_SIZE]
    data = json.dumps(items_chunk).encode()
    response = client.upload_documents(
                                documents=data,
                                contentType='application/json'
                                )
    print('Uploaded.')

print('Done.')

# url http://search-revitapidocs-staging-aikyh7yoyt43gf4wv3pemwlq3i.us-east-1.cloudsearch.amazonaws.com/2013-01-01/
# search?q=filtered
# suggest?q=filtered&suggester=revitapidocs_title
