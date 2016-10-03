from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import ujson
import os
import sys
from pprint import pprint

cwd = os.path.dirname(__file__)

YEARS = ['2015', '2016','2017']
TAGS = [
        'Property', 'Methods', 'Class',
        'Constructor', 'Members', 'Method',
        'Enumeration', 'Events', 'Event', 'Namespace',
        'Interface', 'Properties', 'Delegate']

unique = {}

def clean_string(string):
    # BuiltInFailures.PipingFailures Class
    # "description": "\"%1s is not found. Please review the routing preference of %2s.\"",
    # breakline character
    string = re.sub('\u00a0', ' ', string)
    # New line
    string = re.sub(r'\n', '', string)
    # Multiple spaces
    string = re.sub(r'\s{2,}', ' ', string)
    # BuiltInFailures..::..RegenFailures Class"
    string = string.replace('..::..', '.')
    string = string.replace("'", "'")
    return string

try:
    with open('parser/ns_index.json', 'r') as fp:
        jdata = ujson.load(fp)
except:
    jdata = []

index = {}
for d in jdata:
    index[d['href']] = d

for year in YEARS:
    DIR = 'app/templates/{year}'.format(year=year)

    MAX = None
    # MAX = 20
    for filename in os.listdir(DIR)[0:MAX]:
        # if 'fb011c91-be7e-f737-28c7-3f1e1917a0e0.htm' not in filename:
            # continue
        if not index.get(filename):
            with open(os.path.join(DIR,filename), 'r') as fp:
                content = fp.read()
                # print(content)

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
            try:
                # short
                header = soup.find(id='headerTableRow3')
                if header and 'Also' not in header.text:
                    # print(header.find('a').text)
                    member_of = header.find('a').text.strip()
                    member_of = clean_string(member_of)
                else:
                    member_of = namespace

            except:
                pass

            title = soup.title.string.strip()
            clean_title = ''
            tag_name = None

            for tag in TAGS:
                if tag in title:
                    tag_name = tag
                    clean_title = title.strip()
                    # clean_title = title.split(tag_name)[0].strip()
                    break

            data = {}
            data['href'] = filename
            data['title'] = clean_title or title
            data['tag'] = tag_name
            data['namespace'] = namespace
            data['description'] = description
            data['member_of'] = member_of
            data['year'] = [year]

            index[filename] = data

        else:
            if year not in index[filename]['year']:
                index[filename]['year'].append(year)



flat_index = index.values()
names_in_ns = [entry['title'].split(' ')[0].lower() for entry in flat_index]
# print(names_in_ns)

members_index = {}
filename = 'app/templates/json/members_{year}.json'.format(year=year)
for year in YEARS:
    with open(filename, 'r') as fp:
        members = ujson.load(fp)

    for member in members.keys():
        short_member_name = member.split(' ')[0].lower()
        if 'enumeration member' in short_member_name:
            if not members_index.get(short_member_name):
                data = {}
                href = members[member]
                data['year'] = [year]
                data['title'] = member
                data['href'] = href

                data['namespace'] = index[href]['namespace']
                data['member_of'] = index[href]['title']
                data['description'] = ''

                tag_name = None
                for tag in TAGS:
                    if tag.lower() in member:
                        tag_name = tag
                        break

                data['tag'] = tag_name
                members_index[short_member_name] = data
            else:
                members_index[short_member_name]['year'].append(year)

print(members_index)





# pprint(index)
cwd = os.path.dirname(__file__)
OUTFILE = 'ns_index.json'
os.chdir(cwd)
# print(__file__)
with open(OUTFILE, 'w') as fp:
    ujson.dump(flat_index, fp, indent=1)
# pprint(ul)
