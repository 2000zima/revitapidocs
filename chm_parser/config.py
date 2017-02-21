import os
from collections import namedtuple
CWD = os.getcwd()

DEFAULT_OUT_HTML_DIR = r'chm_parser\data\out_{year}\html'
DEFAULT_OUT_JSON_DIR = r'chm_parser\data\out_{year}'

DEFAULT_DB_INDEX_MERGED_JSON = 'db_index.json'
DEFAULT_DB_INDEX_JSON = 'db_index_{year}.json'
DEAFULT_DB_INDEX_MEMBERS_JSON = 'db_index_members_{year}.json'
DEFAULT_NAMESPACE_JSON = 'namespace_{year}.json'

STATIC_ASSET_EXPRESSION = '{{{{ url_for("static", filename="img/chm/icons/{0}") }}}}'
TEST_CSS_PATH = '../static/packed.css'

YEARS = ['2015', '2016','2017', '2017.1']

# This will be used to try to match agains title, and it's used for filtering
# Entries on search result
TAGS = [
        'Enumeration Member',
        'Enumeration',
        'Members',
        'Class',
        'Method',
        'Property',
        'Methods',
        'Events',
        'Namespace',
        'Event',
        'Interface',
        'Properties',
        'Delegate',
        'Operators', 'Operator',
        'Fields', 'Field',
        'Conversions', 'Conversion',
        'Constructor',
        'Structure'
       ]

AUTODESK_NAMESPACE = 'd4648875-d41a-783b-d5f4-638df39ee413.htm'

# Used to Replace path on html output
replacement = namedtuple('replacement', ['old_pattern', 'new_pattern', 'mandatory'])
replacement_list = (
                      replacement('(on\w+="[^"]+") ', '', False),
                      replacement('(cell\w+="[^"]+") ', '', False),
                    #   replacement(u'\uFEFF', u'', False),
                    )
