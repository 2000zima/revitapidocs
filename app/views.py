import os
import re
from collections import OrderedDict
import requests

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

from app.utils.github_helper import get_repo_data
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
    message = os.getenv('MESSAGE')
    return render_template('index.html', title=title, message=message)


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
    context = {'entry': entry,
               'content_path': content_path,
               'active_href': filename,
               'actual_year': year_best_match,
               'active_year': year,
               }

    if 'ajax' in request.args:
        context['content_html'] = render_template(content_path)
        return jsonify(context)

    return render_template(template, **context)


@app.route('/<string:year>/news', methods=["GET"])
def api_whats_new(year):
    if year not in AVAILABLE_YEARS:
        abort(404)  # File was not found

    template = '_api.html'
    entry = {'member_of': "Revit API {}".format(year),
             'member_of_href': '/{}'.format(year),
             'title': 'API Changes {}'.format(year),
             'description': 'API Changes for the {} API'.format(year),
             }
    content_path = '{}/{}/{}.htm'.format(API_DOCS_NAME, 'news', year)

    return render_template(template, active_year=year, entry=entry,
                           content_path=content_path,
                           active_href=None)


@cache.cached(timeout=3600)  # 1 Hour
@app.route('/<string:year>/namespace.json', methods=['GET'])
def ajax_namespace_get(year):
    namespace_url = url_for('static', filename='json/namespace/{year}_min.json'.format(year=year))
    logger.warning('namespace json view called: {}'.format(namespace_url))
    return redirect(namespace_url)


@app.route('/<string:year>/search', methods=['GET'])
@Timer.time_function('Search')
def search_api(year):
    MAX_RESULTS = 300
    raw_query = request.args.get('query')

    if not raw_query or raw_query == '0':
        return jsonify({'error': 'Invalid Query Param', 'results':[], 'query': raw_query, 'total_results':0})

    final_query = process_query(raw_query)
    final_query_pat = re.compile(final_query, re.IGNORECASE)
    logger.debug('Raw Search Query: ' + str(raw_query))
    logger.debug('Final Search Query: ' + str(final_query_pat))

    results = search_db(pattern=final_query_pat, field='title')

    if not results:
        return jsonify({'error': 'No Results', 'results':[], 'target_year': year, 'query': raw_query})

    sorted_results = sorted(results, key=lambda k: k['title'])
    prioritized_results = prioritize_match(results=sorted_results, raw_query=raw_query, field='title')
    total_results = len(prioritized_results)
    truncated = False
    if total_results > MAX_RESULTS:
        prioritized_results = prioritized_results[:MAX_RESULTS]
        truncated = True

    return jsonify({'results': prioritized_results,
                    'target_year': year,
                    'query': raw_query,
                    'total_results': total_results,
                    'max_results': MAX_RESULTS,
                    'truncated': truncated
                    })


@app.route('/code/', methods=['GET'])
@app.route('/code/<path:path>', methods=['GET'])
def code(path=None):
    entry = {'title': 'Revit API - Code Samples',
             'description': 'Code Samples Repository for the Revit API'}
    return render_template('code.html')


@app.route('/api/code', methods=['GET'])
def code_api():
    repo = get_repo_data()
    return jsonify(repo)

@app.route('/api/constructor_key', methods=['GET'])
def constructor_key_api():
    """ Get Constructor API Key from backend and pass to front end """
    key = app.config['CONSTRUCTOR_IO_AUTOCOMPLETE_KEY']
    return jsonify(key)

@app.route('/api/insights', methods=['GET'])
def api_python_insights():
    # Wall user:gtalarico user:eirannejad user:andydandy74 user:dimven user:ksobon language:Python extension:py language:Python
    SEARCH_URL = 'https://api.github.com/search/code?q={query}+in:file+language:Python+extension:py{users}'

    token = os.getenv('GITHUB_TOKEN')
    query = request.args.get('query')
    language = request.args.get('language', 'Python')
    user = request.args.get('language', 'gtalarico')
    headers = {'Authorization': 'token {}'.format(token),
               'Accept': 'application/vnd.github.v3.text-match+json'}

    users = ['andydandy74', 'gtalarico', 'eirannejad', 'dimven', 'ksobon']
    users = ''.join(['+user:{}'.format(u) for u in users])
    url = SEARCH_URL.format(query=query, lang=language, users=users)
    MAX = 10
    req = requests.get(url, headers=headers)
    json_data = req.json()
    results = json_data.get('items', [])[:MAX]
    response = {'results': results, url: url}

    return jsonify(response)


@app.after_request
def add_header(response):
    config_cache = app.config['SEND_FILE_MAX_AGE_DEFAULT']
    response.headers['Cache-Control'] = 'public, max-age={}'.format(config_cache)
    return response


# This handles the static files form the .CHM content
@cache.cached(timeout=86400)
@app.route('/favicon.ico', methods=["GET"])
def chm_static_redirect(filename=None):
    path = '/static' + request.path
    return redirect(path, 301)
