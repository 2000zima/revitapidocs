""" Boostraps final html folder by copying over required files
based on the db_index.json.

For example, if a file exists in 2015, but remains unchanged in 2015 > 2017,
only the 2015 version is copied.

If the files is new, or is updated, a new file is copied.

The logic for whether a file has changed or not is defined in the
merge parser.

"""

import os
from collections import defaultdict
from pprint import pprint
import difflib
import shutil

from logger import logger

from .utils import open_html, load_json
from .html_parser import parse_soup, make_soup
from .config import YEARS, DEAFULT_DB_INDEX_MEMBERS_JSON


def _copy_helper(filename, year, out_html_dir, out_merge_dir):
    html_folder_name = 'out_{year}'.format(year=year)
    hmtl_directory = os.path.join(out_html_dir, html_folder_name, 'html')
    out_directory = os.path.join(out_merge_dir, year)
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
    src = os.path.join(hmtl_directory, filename)
    dst = os.path.join(out_directory)
    shutil.copy2(src, dst)
    # logger.info('Copying: {} > {}'.format(src, dst))


def bootstrap(db_index_path, out_html_dir, out_merge_dir):
    db_index = load_json(db_index_path)
    for member_key, member in db_index.items():
        if '2015' in member['years']:
            _copy_helper(member['href'], '2015', out_html_dir, out_merge_dir)

        for year, status in sorted(member['years'].items(), key=lambda x: x):
            if status == 'exists' or status == 'updated':
                _copy_helper(member['href'], year, out_html_dir, out_merge_dir)
            if status == 'unchanged':
                continue
