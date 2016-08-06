from bs4 import BeautifulSoup
from collections import OrderedDict
import re

FILE = 'app/templates/ns_2015.html'
OUTFILE = 'OUT.json'
with open(FILE, 'r') as fp:
    content = fp.read()

def dictify(ul):
    # result = {}
    result = OrderedDict()
    li = ul.find("li")
    # if li:
    print(ul)
    a = li.find('a')
    try:
        result['text'] = a.text
    except:
        import pdb; pdb.set_trace()
    result['href'] = a['href']
    result['nodes'] = [dictify(ul_child) for ul_child in ul.find_all("ul", recursive=False)]
    return result

    # return result

soup = BeautifulSoup(content, 'html.parser')
# soup = BeautifulSoup(content, 'html5lib')
ul = soup.ul

r = dictify(ul)
import json
# with open(OUTFILE, 'w') as fp:
    # json.dump(r, fp, indent=1)
# pprint(ul)