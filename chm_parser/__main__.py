
import sys
import os
import re
import json
import time
from pprint import pprint
from bs4 import BeautifulSoup
from docopt import docopt

sys.path.append('./app/utils')
from logger import logger

from .html_parser import make_soup, parse_soup, batch_replacement
from .hhc_parser import parse_namespace
from .hhk_parser import parse_members, extract_enumeration_descriptions
from .bootstrap import bootstrap
from .upload_autocomplete import upload
from .merger import merge
from .news_parser import parse_news
from .utils import open_html, write_html, dump_json, load_json, Timer
from .config import replacement_list
from .config import DEFAULT_OUT_HTML_DIR, DEFAULT_OUT_JSON_DIR
from .config import DEFAULT_DB_INDEX_JSON, DEAFULT_DB_INDEX_MEMBERS_JSON, DEFAULT_NAMESPACE_JSON, DEFAULT_DB_INDEX_MERGED_JSON

__doc__ = """
    Revit API CHM Parser.

    Usage:
      chm_parser parse_pages <year> <in-html-dir> [--output=<DIR>] [--json-directory=<DIR>]
                                [--start-index=<INT>] [--end-index=<INT>] [--no-minify]
                                [--no-html] [--no-json] [--html-test-mode] [--single-file=<FILE>]
      chm_parser parse_namespaces <year> <hhc-filepath> [--json-directory=<DIR>] [--no-minify]
      chm_parser parse_members <year> <hhk-filepath> <in-html-dir> <db-index-filepath> [--json-directory=<DIR>] [--no-minify]
                                                                                       [--no-html] [--no-json]
      chm_parser merge <out-2015> [--no-json]
      chm_parser bootstrap <out-html-dir> <db-index.json> <out-merge-dir>
      chm_parser parse_news <year> <whastnew> [--output=<DIR>]
      chm_parser upload <db-index.json>
      chm_parser -h | --help
      chm_parser --version

    Options:
      --output DIR           Html output directory [default: {default_out_dir}].
      --json-directory DIR   Json output directory filepath [default: {json_out_dir}].
      --no-minify            Disable minify output [default: False].
      --start-index INT      Start index [default: ].
      --end-index INT        End index [default: ].
      --single-file FILE     Testing Mode. Injects <html> and other tags.
      --html-test-mode       Testing Mode. Injects <html> and other tags [default: False].
      --no-json              Don't write json file [default: False].
      --no-html              Don't write html files [default: False].
      -h --help              Show this screen.

    """.format(default_out_dir=DEFAULT_OUT_HTML_DIR,
               json_out_dir=DEFAULT_OUT_JSON_DIR)

__version__ = '1.0.0'
arguments = docopt(__doc__, version=__version__)
# logger.info(arguments)

# Global Option
minify_json = not arguments['--no-minify']
year = arguments['<year>']
out_json_dir = arguments['--json-directory'].format(year=year)

make_html = not arguments['--no-html']
make_json = not arguments['--no-json']

if arguments['--start-index']:
    MIN = int(arguments['--start-index'])
else:
    MIN = None
if arguments['--end-index']:
    MAX = int(arguments['--end-index'])
else:
    MAX = None

############################
# UPLOAD TO CONSTRUCTOR.IO #
############################
if arguments['upload']:
    db_index_path = arguments['<db-index.json>']
    upload(db_index_path)


##############
# PARSE NEWS #
##############
if arguments['parse_news']:
    whatsnew_html_path = arguments['<whastnew>']
    out_whatsnew_html = arguments['--output'].format(year=year)

    soup = parse_news(whatsnew_html_path)
    filename = '{year}.htm'.format(year=year)
    write_html(soup.prettify(), filename, directory=out_whatsnew_html)

    print('Done.')

############################
# Bootstrap #
############################
if arguments['bootstrap']:
    timer = Timer()

    out_html_dir = arguments['<out-html-dir>']
    db_index_path = arguments['<db-index.json>']
    out_merge_dir = arguments['<out-merge-dir>']

    bootstrap(db_index_path, out_html_dir, out_merge_dir)

    print('Done: {} seconds'.format(timer.stop()))

############################
# MERGE DOCS               #
############################
if arguments['merge']:
    timer = Timer()

    out_sample = arguments['<out-2015>']
    db_index_merged = merge(out_sample)

    out_json_dir = out_json_dir.replace('None', 'Merged')
    json_filepath = os.path.join(out_json_dir, DEFAULT_DB_INDEX_MERGED_JSON)

    if make_json:
        dump_json(db_index_merged, json_filepath, indent=1, minify=minify_json)
    else:
        logger.info('JSON was not built (--no-json)')

    print('Done: {} seconds'.format(timer.stop()))
    print('{} items'.format(len(db_index_merged)))

############################
# PARSE HHC - NAMESPACES   #
############################
# Less then 1 minutes
if arguments['parse_namespaces']:
    in_hhc_filepath = arguments['<hhc-filepath>']

    hhc_html = open_html(in_hhc_filepath)
    hhc_json_data = parse_namespace(hhc_html)
    json_filepath = os.path.join(out_json_dir, DEFAULT_NAMESPACE_JSON.format(year=year))

    if make_json:
        dump_json(hhc_json_data, json_filepath, indent=1, minify=minify_json)

############################
# PARSE HHK - MEMBERS      #
############################
# About 30 seconds
if arguments['parse_members']:
    timer = Timer()
    in_hhk_filepath = arguments['<hhk-filepath>']
    in_html_dir = arguments['<in-html-dir>']
    db_index_filepath = arguments['<db-index-filepath>']
    db_index = load_json(db_index_filepath)

    hhk_html = open_html(in_hhk_filepath)
    members_index = parse_members(hhk_html, db_index)
    members_index_w_description = extract_enumeration_descriptions(members_index, in_html_dir)

    db_index.update(members_index_w_description)
    json_filepath = os.path.join(out_json_dir, DEAFULT_DB_INDEX_MEMBERS_JSON.format(year=year))

    if make_json:
        dump_json(db_index, json_filepath, indent=1, minify=minify_json)

    print('Done: {} seconds'.format(timer.stop()))
    print('{} items'.format(len(members_index)))

############################
# PARSE HTML DIR           #
############################
# About 10 minutes
if arguments['parse_pages']:
    timer = Timer()
    # Required
    in_html_dir = arguments['<in-html-dir>']
    out_html_dir = arguments['--output'].format(year=year)

    logger.info('Finding files in: {}'.format(in_html_dir))

    # Options
    testing = arguments['--html-test-mode']
    single_file = arguments['--single-file']
    if testing:
        out_html_dir += '_testing'

    members = {}
    filenames = sorted(os.listdir(in_html_dir))[MIN:MAX]
    total = len(filenames)
    for n, filename in enumerate(filenames):
        if single_file and filename not in single_file:
            continue
        if not filename.endswith('.htm'):
            logger.warning('File is not .htm. Skipping.')
            continue

        logger.info('Parsing [{}]:{}/{}'.format(filename, n, total))
        html_content = open_html(filename, directory=in_html_dir)

        raw_soup = make_soup(html_content)
        soup, member = parse_soup(raw_soup, filename, testing=testing)

        href = member['href']
        members[href] = member
        final_html = batch_replacement(soup.prettify(), replacement_list)
        # final_html = soup.prettify().encode('ascii', errors=i).decode('utf-8-sig')

        if make_html:
            write_html(final_html, filename, directory=out_html_dir)
        # Add Year Key [m.update({'year': [year]}) for m in members.values()]

    if make_json:
        json_filepath = os.path.join(out_json_dir, DEFAULT_DB_INDEX_JSON.format(year=year))
        dump_json(members, json_filepath, indent=1, minify=minify_json)

    print('Done: {} seconds'.format(timer.stop()))
    print('{} items'.format(len(filenames)))
    logger.info('Output folder: {}'.format(out_html_dir))


if not make_html or not make_json:
    logger.info('Json or Html were not made. Make sure arguments are correct.')

sys.exit(0)
