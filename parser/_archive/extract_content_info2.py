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
    try:
        header = soup.find(id='headerTableRow3')
        # if header and 'Also' not in header.text:
        if header:
            a = header.find('a')
            member_of = a.text.strip()
            member_of = clean_string(member_of)
            if 'Also' in member_of:
                member_of = namespace
            member_of_href = a.get('href')
        else:
            raise Exception('Check this out')

    except:
        pass

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
    with open('parser/ns_index3.json', 'r') as fp:
        jdata = ujson.load(fp)
except:
    jdata = []

index = {}

count = 0
MAX = 100000
members_index = {}
for year in YEARS:
    filename = 'app/templates/json/members_{year}.json'.format(year=year)
    with open(filename, 'r') as fp:
        members = ujson.load(fp)

    for member, href in members.items():
        if 'pushbutton' not in member.lower():
            continue
        if count > MAX: break

        data_page = get_data_from_href(href, year)
        short_member_name = member.split(' ')[0].lower()

        if members_index.get(short_member_name):
            members_index[short_member_name]['year'].append(year)
            continue

        #member is namespace
        if 'enumeration member' not in member.lower():
            data_page['type'] = 'namespace'
            members_index[short_member_name] = data_page
            print('Added NS:', member)

        else:
            # name_wihout_ns = member.split(data_page['namespace'])[-1].strip()
            # if members_index.get(name_wihout_ns):
                # print('Skipping: ', name_wihout_ns)
                # continue
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
            count += 1
            print('Added Member: ', member)
        # else:
            # print(short_member_name)
            # print('not in :', data_page['title'].split(' ')[0].lower())


flat_members_index = members_index.values()
# pprint(index)
cwd = os.path.dirname(__file__)
OUTFILE = 'ns_index3.json'
os.chdir(cwd)
# print(__file__)
with open(OUTFILE, 'w') as fp:
    ujson.dump(flat_members_index, fp, indent=1)
# pprint(ul)