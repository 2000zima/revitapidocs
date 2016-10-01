from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import ujson
import os
import sys
from pprint import pprint

cwd = os.path.dirname(__file__)

YEARS = ['2015', '2016','2017']
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


OUTFILE = 'index_dump.json'

index = {}

for year in YEARS:
    DIR = 'app/templates/{year}'.format(year=year)

    MAX = None
    MAX = None
    for filename in os.listdir(DIR)[0:MAX]:

        if not index.get(filename):
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
            try:
                # short
                header = soup.find(id='headerTableRow3')
                if header and 'Also' not in header:
                    # print(header.find('a').text)
                    member_of = header.find('a').text.strip()
                    member_of = clean_string(member_of)

            except:
                pass

            title = soup.title.string.strip()
            clean_title = ''
            tag_name = None
            allowed_tags = ['Property', 'Methods', 'Class', 'Constructor', 'Members', 'Method']
            for tag_name in allowed_tags:
                if tag_name in title:
                    tag_name = tag_name
                    clean_title = title.split(tag_name)[0].strip()
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
            index[filename]['year'].append(year)


# pprint(index)
cwd = os.path.dirname(__file__)
os.chdir(cwd)
# print(__file__)
with open(OUTFILE, 'w') as fp:
    ujson.dump(index, fp, indent=1)
# pprint(ul)
