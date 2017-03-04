''' Creates db_index.json.

This is used as the primary file for search and Getting
metadata about shown pages without having to
scrape page everytime.

Json file is loaded as a dictionary.
href is used for entries that are their own pages (type: namespace).
Short Title name is used for entries that don't have their own page
ie: enumeration member (type: member).
These are enties in the member namespace list that are part of another entry

[

    "d854e0db-0621-3288-82b0-1be4b9976a0d.htm":{
      "year":[
       "2015",
       "2016",
       "2017"
      ],
      "type":"namespace",
      "member_of_href":"6f2d8dc7-6a19-fba3-00ae-a88cfe0e3d34.htm",
      "description":"Returns true if the properties CreatedPhaseId and DemolishedPhaseId can be modified for this Element.",
      "title":"CutMarkType Members",
      "member_of":"CutMarkType Class",
      "namespace":"Autodesk.Revit.DB.Architecture",
      "tag":"Members",
      "href":"d854e0db-0621-3288-82b0-1be4b9976a0d.htm"
     }
 ...
]

'''

from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import ujson
import os
import sys
from pprint import pprint
import time

t1 = time.time()

cwd = os.path.dirname(__file__)

YEARS = ['2015', '2016','2017']
TAGS = [
        'Property', 'Methods', 'Class',
        'Constructor', 'Members', 'Method',
        'Enumeration', 'Events', 'Event', 'Namespace',
        'Interface', 'Properties', 'Delegate']


def clean_string(string):
    # BuiltInFailures.PipingFailures Class
    # "description": "\"%1s is not found. Please review the routing preference of %2s.\"",
    # breakline character
    string = re.sub('\u00a0', ' ', string)
    string = re.sub(r'\n', '', string)
    # Multiple spaces
    string = re.sub(r'\s{2,}', ' ', string)
    # BuiltInFailures..::..RegenFailures Class"
    string = string.replace('..::..', '.')
    string = string.replace("'", "'")
    return string


def get_data_from_href(filename, year):
    DIR = 'app/templates/{year}'.format(year=year)


    with open(os.path.join(DIR,filename), 'r') as fp:
        content = fp.read()

    soup = BeautifulSoup(content, 'html.parser')
    metas = soup.find_all('meta')
    for meta in metas:
        if meta.get('name') == 'container':
            namespace = meta['content'].strip()

    try:
        # short
        description = soup.find(id='mainBody').find('div', { "class": "summary"}).text.strip()
        description = clean_string(description)
    except:
        description = ''

    member_of = ''
    # try:
    header = soup.find(id='headerTableRow3')
    # if header and 'Also' not in header.text:
    if header:
        a = header.find('a')
        member_of = a.text.strip()
        member_of = clean_string(member_of)
        if 'Also' not in member_of:
            member_of_href = a.get('href')
        else:
            member_of = namespace
            # member_of_href = '#'
            try:
                member_of_href = soup.find(id='mainBody').find('a').get('href')
            except:
                member_of_href = '#'
    else:
        raise Exception('Check this out')


    title = soup.title.string.strip()
    clean_title = ''
    tag_name = None

    for tag in TAGS:
        if tag in title:
            tag_name = tag
            clean_title = title.strip()
            break

    data = {}
    data['href'] = filename
    data['title'] = clean_title or title
    data['tag'] = tag_name
    data['namespace'] = namespace
    data['description'] = description
    data['member_of'] = member_of
    data['member_of_href'] = member_of_href
    data['year'] = [year]

    return data

try:
    with open('parser/ns_index4.json', 'r') as fp:
        jdata = ujson.load(fp)
except:
    jdata = []

count = 0
MAX = 110000000
# MAX = 30
MAX_YEAR = 1
MAX_YEAR = None
# MAX = None
# members_index = jdata
members_index = {}

for year in YEARS[0:MAX_YEAR]:
    DIR = 'app/templates/{year}'.format(year=year)
    for filename in os.listdir(DIR)[0:MAX]:
        if 'new_' in filename:
            continue
        # print('Adding: ', filename)
        data_page = get_data_from_href(filename, year)
        href = filename

        if members_index.get(href) and 'year' not in members_index[href]['year']:
            members_index[href]['year'].append(year)
            continue

        else:
            data_page['type'] = 'namespace'
            members_index[href] = data_page
    print('Done {} Namespace.'.format(year))

print('Done Namespaces. Starting members...')

for year in YEARS[0:MAX_YEAR]:
    filename = 'app/templates/json/members_{year}.json'.format(year=year)
    with open(filename, 'r') as fp:
        members = ujson.load(fp)

    for member, href in members.items():
        pat = re.compile('enumeration member', flags=re.IGNORECASE)
        match = re.search(pat, member)
        if not match:
            # print('Skipping')
            continue
        else:
            data_page = get_data_from_href(href, year)
            short_member_name = member.split(' ')[0].lower()

            if members_index.get(short_member_name) and year not in members_index[short_member_name]['year']:
                members_index[short_member_name]['year'].append(year)


            else:
                data = {}
                data['year'] = [year]
                data['title'] = member
                data['href'] = href

                data['namespace'] = data_page['namespace']
                data['member_of'] = data_page['title']
                data['member_of_href'] = href  # will match when member
                data['type'] = 'member'

                tag_name = None
                for tag in TAGS:
                    if tag.lower() in member:
                        tag_name = tag
                        break

                data['description'] = ''
                data['tag'] = tag_name
                members_index[short_member_name] = data
                # print('Member Added: ', member)

    print('Done {} Members.'.format(year))



flat_members_index = members_index.values()
# pprint(index)
cwd = os.path.dirname(__file__)
OUTFILE = 'ns_index4.json'
OUTFILE_DICT = 'ns_index4_dict.json'
os.chdir(cwd)
# print(__file__)
duration = time.time() - t1
print('Done: ', duration)

with open(OUTFILE_DICT, 'w') as fp:
    ujson.dump(members_index, fp, indent=1)

with open(OUTFILE, 'w') as fp:
    ujson.dump(flat_members_index, fp, indent=1)
# pprint(ul)
