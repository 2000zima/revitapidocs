import os
import sys
import json
import re
import requests
from collections import OrderedDict

from flask import render_template, redirect, url_for, send_from_directory
from flask import request
from flask import abort, flash, jsonify
from jinja2.exceptions import TemplateNotFound

from app import app
from app import cache
from app.logger import logger
from app.utils import AVAILABLE_APIS
from app.utils import get_schema, check_available_years, Timer
from app.utils import create_permutation_query, search_db
from app.gists import get_gists
from app.db import db_json


@cache.cached(timeout=600)
@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    return render_template('index.html', title=title)

# API Pages: /2015/123sda-asds-asd.htmll
@cache.cached(timeout=600)
@app.route('/<string:year>/', methods=["GET"])
@app.route('/<string:year>/<path:filename>', methods=["GET"])
def api_year(year, filename=None):
    """Add Docs"""
    template = 'api.html'

    if filename:
        content_path = '{year}/{html}'.format(year=year, html=filename)
        schema = get_schema(filename, year=year)
        available_in = check_available_years(filename)
        if available_in and year not in available_in:
            # file exists but not year requested
            template = 'missing.html'

    elif not filename and year in AVAILABLE_APIS:
        content_path = 'home.html'
        available_in = check_available_years(filename)
        schema = {'title': "Revit API {} Index".format(year),
                  'description': 'Full Online Documentation for Revit API {}'.format(year)}

    else:
        abort(404)
    try:
        return render_template(template, year=year, active_href=filename,
                               content=content_path, available_in=available_in,
                               schema=schema)

    except TemplateNotFound as error:
        """Must handle it since { include } inside template is generated
        dynamically by request path"""
        logger.error('Template not found. Path: %s', request.path)
        abort(404)


@cache.cached(timeout=604800)  # 1 Week
@app.route('/<string:year>/namespace.json', methods=['GET'])
def namespace_get(year):
    cwd = app.config['BASEDIR']
    filename = 'ns_{year}.json'.format(year=year)
    fullpath = '{}/{}/{}/{}'.format(cwd, app.template_folder,
                                    'json', filename)
    with open(fullpath) as fp:
        j = json.load(fp)
    return jsonify(j)


@app.route('/<string:year>/searchapi', methods=['GET'])
def search_api(year):
    t = Timer()
    MAX_RESULTS = 500
    query = request.args.get('query')

    if not query or query == '0':
        return jsonify({'error': 'Invalid Query Param'})

    query = create_permutation_query(query)

    final_query_pat = re.compile(query, re.IGNORECASE)
    logger.debug('Search Query: ' + str(final_query_pat))
    results = search_db(final_query_pat, 'title')

    if not results: return jsonify({'error': 'No Results'})

    sorted_results = sorted(results, key=lambda k: k['title'])
    if len(sorted_results) > MAX_RESULTS:
        # flash('Results Truncated to 300. Try narrowing your search.')
        sorted_results = sorted_results[:MAX_RESULTS]
    logger.debug('*** TIME [API SEARCH]: ' + str(t.stop()))
    return jsonify(sorted_results)


# This handles the static files form the .CHM content
@cache.cached(timeout=86400)
@app.route('/favicon.ico', methods=["GET"])
@app.route('/icons/<string:filename>', methods=["GET"])
@app.route('/scripts/<string:filename>', methods=["GET"])
@app.route('/styles/<string:filename>', methods=["GET"])
def chm_static_redirect(filename=None):
    path = '/static' + request.path
    return redirect(path, 301)


@app.after_request
def add_header(response):
    config_cache = app.config['SEND_FILE_MAX_AGE_DEFAULT']
    response.headers['Cache-Control'] = 'public, max-age={}'.format(config_cache)
    return response


@app.route('/python/', methods=['GET'])
def python():
    gists_by_categories = get_gists()
    d = OrderedDict(sorted(gists_by_categories.items()))
    schema = {'title': 'Revit API - Python',
              'description': 'Python Examples for the Revit API'}
    return render_template('python.html', gists_categories=d, schema=schema)
