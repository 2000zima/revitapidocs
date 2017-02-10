''' Script to batch update index to Contructor.io
autocomplete api.
'''

import time
import requests
import os
import json
import csv

db = os.path.join('app', 'templates', 'json', 'db_index.json')

with open(db) as fp:
    jdata = json.load(fp)

items = []
unique_names = {}

for n, i in enumerate(jdata.values()):
    title = i['title']

    if title in unique_names:
        continue

    item = {}
    score = 1
    tag = i['tag']
    if tag and 'class' in tag.lower():
        score += 1
    # if ['description'] != '':
    #     score += 1
    if ['namespace'] == 'Autodesk.Revit.UI' or ['namespace'] == 'Autodesk.Revit.DB':
        score += 1
    description = i['description']


    item['item_name'] = title
    item['autocomplete_section'] = 'Search Suggestions'
    item['suggested_score'] = score
    item['id'] = str(title)
    items.append(item)
    unique_names[title] = True


# from pprint import pprint
# pprint(items)

import sys
import os
# sys.exit()
t1 = time.time()


headers = {"Content-Type": "application/json"}

api_key = os.getenv('CONSTRUCTOR_IO_API_TOKEN')
autocomplete_key = os.getenv('CONSTRUCTOR_IO_AUTOCOMPLETE_KEY')
auth = (api_key, '')

# Also tried:
# item = '{'item_name': 'PROJECT_BUILDING_NAME enumeration member',
#          'autocomplete_section': 'Search Suggestions',
#          'suggested_score': '1'}'



url = "https://ac.cnstrc.com/v1/verify?autocomplete_key={key}".format(key=autocomplete_key)
r = requests.get(url, headers=headers, auth=auth)
print(r)
# >>> <Response 200>
if r.status_code == 200:
    print('AUTHORIZATION SUCCESSFUL')

print('Uploading items: {}'.format(len(items)))
errors = []
CHUNK_SIZE = 1000
for i in range(0, len(items), CHUNK_SIZE):
    items_chunk = items[i:i+CHUNK_SIZE]
#
    unique_items = set(i['item_name'] for i in items_chunk)
#
    print('Uploading data set: {}'.format(len(items_chunk)))
    print('Unique Items: {}'.format(len(unique_items)))
#
#
    payload = {'items': items_chunk,
               'autocomplete_section': 'Search Suggestions'
               }

    url = "https://ac.cnstrc.com/v1/batch_items?force=1&autocomplete_key={key}".format(key=autocomplete_key)
    r = requests.put(url, headers=headers, auth=auth, json=payload)
    if r.status_code == 204:
        print('<STATUS 204> Data Updated')
        # print('<STATUS 204> Data Updated: {}'.format(item['item_name']))
    else:
        response = r.json()
        print('<STATUS {}>: {}'.format(r.status_code, response['message']))
        errors.append('batch:' + str(i))
        break

t2 = time.time()

print('Done: {} seconds'.format(t2 - t1))
print('Errors: {}'.format(len(errors)))
print(errors)
