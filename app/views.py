import os
import re
from collections import OrderedDict

from flask import render_template, redirect, url_for, send_from_directory
from flask import request
from flask import abort, flash, jsonify
from jinja2.exceptions import TemplateNotFound

from app import app
from app import cache
from app.utils.db import db_json, namespace_jsons

from app.utils.db_utils import search_db
from app.utils.db_utils import get_entry, get_best_entry_match
from app.utils.db_utils import process_query, prioritize_match

from app.utils.gists import get_gists
from app.utils.misc import Timer
from app.utils.logger import logger

AVAILABLE_YEARS = app.config['AVAILABLE_APIS']
API_DOCS_PATH = app.config['API_DOCS_PATH']
API_DOCS_NAME = app.config['API_DOCS_NAME']


@cache.cached(timeout=600)
@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    return render_template('index.html', title=title)


@cache.cached(timeout=600)
@app.route('/<string:year>/', methods=["GET"])
def content_year_home(year):
    """ Home of api years. Inserts home.html into api.html base"""
    template = '_api.html'
    if year not in AVAILABLE_YEARS:
        abort(404)

    filename = 'home.html'
    entry = {'title': 'Revit API {}'.format(year),
             'member_of': 'Home',
             'member_of_href': '',
             'description': 'Full Online Documentation for Revit API {}'.format(year),
             }

    return render_template(template, active_year=year, content_path=filename, entry=entry)


@app.route('/<string:year>/<path:filename>', methods=["GET"])
def content_year_file(year, filename):
    """ API Doc Router. Inserts xxx-xxx.html into api.html base"""
    template = '_api.html'
    entry = get_entry(filename)

    if year not in AVAILABLE_YEARS or not entry:
        abort(404)  # File was not found

    year_best_match = get_best_entry_match(entry, year)
    if not year_best_match:
        # file exists but not year requested
        template = 'missing.html'

    content_path = '{}/{}/{}'.format(API_DOCS_NAME, year_best_match, filename)

    return render_template(template, active_year=year, active_href=filename,
                           content_path=content_path, api_availability=entry['years'],
                           entry=entry, actual_year=year_best_match)

# TEST CONTENT API
@app.route('/<string:year>/api/<path:filename>', methods=["GET"])
def api_year_file(year, filename):
    """ API Doc Router. Inserts xxx-xxx.html into api.html base"""
    template = '_api.html'
    entry = get_entry(filename)

    if year not in AVAILABLE_YEARS or not entry:
        return {'error': 'invalid year'}

    year_best_match = get_best_entry_match(entry, year)

    if not year_best_match:
        # file exists but not year requested
        return {'error': 'missing'}

    content_path = '{}/{}/{}'.format(API_DOCS_NAME, year_best_match, filename)
    # with open(content_filepath) as fp:
    #     content_html = fp.read()

    return jsonify({'content_html': render_template(content_path),
                    'entry': entry,
                    'years': entry['years'],
                    'actual_year': year_best_match,
                    'content_path': content_path})


@app.route('/<string:year>/news', methods=["GET"])
def api_whats_new(year):
    template = '_api.html'
    entry = {'member_of': "Revit API {}".format(year),
             'member_of_href': '/{}'.format(year),
             'title': 'API Changes'.format(year),
             'description': 'API Changes for the {} API'.format(year),
             }
    content_path = '{}/{}/{}.htm'.format(API_DOCS_NAME, 'news', year)

    return render_template(template, active_year=year, entry=entry,
                           content_path=content_path,
                           active_href=None)


@cache.cached(timeout=3600)  # 1 Hour
@app.route('/<string:year>/namespace.json', methods=['GET'])
def ajax_namespace_get(year):
    namespace_json_year = namespace_jsons.get(year)
    if namespace_json_year:
        return jsonify(namespace_json_year)
    else:
        abort(404)


@app.route('/<string:year>/searchapi', methods=['GET'])
def search_api(year):
    MAX_RESULTS = 500
    raw_query = request.args.get('query')

    if not raw_query or raw_query == '0':
        return jsonify({'error': 'Invalid Query Param'})

    final_query = process_query(raw_query)
    final_query_pat = re.compile(final_query, re.IGNORECASE)
    logger.debug('Raw Search Query: ' + str(raw_query))
    logger.debug('Final Search Query: ' + str(final_query_pat))

    results = search_db(pattern=final_query_pat, field='title')

    if not results:
        return jsonify({'error': 'No Results'})

    sorted_results = sorted(results, key=lambda k: k['title'])
    prioritized_results = prioritize_match(results=sorted_results, raw_query=raw_query, field='title')
    if len(prioritized_results) > MAX_RESULTS:
        prioritized_results = prioritized_results[:MAX_RESULTS]
    return jsonify(prioritized_results)


@app.route('/python/', methods=['GET'])
@app.route('/python/<path:path>', methods=['GET'])
def python(path=None):
    gists_by_categories = get_gists()
    d = OrderedDict(sorted(gists_by_categories.items()))
    # import pdb; pdb.set_trace()
    entry = {'title': 'Revit API - Python',
             'description': 'Python Examples for the Revit API'}
    return render_template('python.html', gists_categories=d, entry=entry)


@app.after_request
def add_header(response):
    config_cache = app.config['SEND_FILE_MAX_AGE_DEFAULT']
    response.headers['Cache-Control'] = 'public, max-age={}'.format(config_cache)
    return response


# This handles the static files form the .CHM content
# @cache.cached(timeout=86400)
# @app.route('/favicon.ico', methods=["GET"])
# def chm_static_redirect(filename=None):
    # path = '/static' + request.path
#     return redirect(path, 301)
