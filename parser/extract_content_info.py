from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json
import os
import sys

DIR = 'app/templates/{year}'.format(year=2015)
os.chdir(DIR)

class Article():
    def __init__(self, **kwargs):
        data =kwargs

    def __repr__(self):
        return '<ARTICLE: {}>'.format(str(data))

index = {}

OUTFILE = 'index_dump.json'



for filename in os.listdir():
    with open(filename, 'r', encoding='utf-8') as fp:
        content = fp.read()

    soup = BeautifulSoup(content, 'html.parser')
    metas = soup.find_all('meta')
    for meta in metas:
        if meta.get('name') == 'container':
            namespace = meta['content'].strip()



    try:
        # short
        description = soup.find(id='mainBody').find('div', { "class": "summary"}).text.strip()
    except:
        description = ''
    try:
        # short
        header = soup.find(id='headerTableRow3')
        if header and 'Also' not in header:
            member_of = header.find('a').text.strip()

    except:
        member_of = None

    title = soup.title.string.strip()
    clean_title = None
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
    data['year'] = str(2015)


    index[title] = data




with open(OUTFILE, 'w') as fp:
    json.dump(index, fp, indent=1, ensure_ascii=False)
# pprint(ul)
