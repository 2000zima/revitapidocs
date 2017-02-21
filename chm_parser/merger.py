""" Merges all db__member_index into one single file: db_inde

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

from logger import logger

from .utils import open_html, load_json
from .html_parser import parse_soup, make_soup
from .config import YEARS, DEAFULT_DB_INDEX_MEMBERS_JSON


def _process_folders(out_sample_path):
    """ Process folders to create all paths from the 2015 sample path.
    Basically just replaces 2015 for other years, and in for out.

    IN: out_sample_path

    in_folders = {'2015': chm_parser/data/in_2015,
                   '2016': chm_parser/data/in_2016,
                    etc}

    out_folders = {'2015': chm_parser/data/out_2015,
                   '2016': chm_parser/data/out_2016,
                    etc}
    """
    out_folders = {}
    for year in YEARS:
        out_folders[year] = out_sample_path.replace('2015', year)

    return out_folders


def html_has_changed(member, next_member, current_year, next_year, out_folders):
    """ Compares 2 html files.
    returns True if there is basic attributes don't match, or if
    diff ratio is beyond lower than 0.99
    """

    basic_match = all(((member['title'] == next_member['title']),
                   (member['description'] == next_member['description']),
                   (member['namespace'] == next_member['namespace']),
                    ))

    # if basic parameters don't match, skip, proceed to check html content.
    if not basic_match:
        return True

    # If passed basic test, and is member_type: Enumeration Member, Make it same.
    if member['type'] == 'member':
        return False

    html_filepath1 = os.path.join(out_folders[current_year], 'html', member['href'])
    html_filepath2 = os.path.join(out_folders[next_year], 'html', member['href'])

    html_content1 = open_html(html_filepath1)
    html_content2 = open_html(html_filepath2)

    diff = difflib.SequenceMatcher(None, html_content1.split('\n'), html_content2.split('\n'))
    diff_ration = diff.quick_ratio()
    if diff_ration > 0.99:
        return False
    else:
        return True

def merge(out_sample_path):
    """ Merge db_index_outputs
    db_index_by_year = {'2015': db_index_2015_json_data,
                        '2016': db_index_2015_json_data,
                         etc}
    """
    db_index_by_year = {}

    out_folders = _process_folders(out_sample_path)
    for year, path in out_folders.items():
        db_index_json_filename = DEAFULT_DB_INDEX_MEMBERS_JSON.format(year=year)
        db_index_json_path = os.path.join(path, db_index_json_filename)
        db_index_by_year[year] = load_json(db_index_json_path)

    db_index_merged = {}

    for n_year, current_year in enumerate(YEARS):
        next_year_index = n_year + 1
        if next_year_index == len(YEARS):
            break
        current_year
        next_year = YEARS[next_year_index]

        for member_key, member in db_index_by_year[current_year].items():
            logger.info('Merging: {}:{} | {}'.format(current_year, next_year, member_key))

            # Tries to retrieve entry, if not present, load first member
            member_db_index_merged = db_index_merged.get(member_key)
            if not member_db_index_merged:
                db_index_merged[member_key] = member_db_index_merged = member # <<<

            years_dict_member = member_db_index_merged.get('years', {current_year: 'exists'})
            years_dict_next_member = {}

            next_member = db_index_by_year[next_year].get(member_key)
            if not next_member:
                pass
                # years_dict_member[next_year] = 'not_exists'
                # This works, but doesn't add to previous year
                # So not_exists will just be represented by lack of key
            else:
                if html_has_changed(member, next_member, current_year, next_year, out_folders):
                    years_dict_next_member[next_year] = 'updated'
                else:
                    years_dict_next_member[next_year] = 'unchanged'

            combined_years_dict = years_dict_member.copy()
            combined_years_dict.update(years_dict_next_member)

            years_db_index_merged = member_db_index_merged.get('years', {})
            member_db_index_merged['years'] = combined_years_dict

            db_index_merged[member_key] = member_db_index_merged

            # print(db_index_merged)
            # db_index_merged.get(member_key, {}).update(combined_member)

    return db_index_merged