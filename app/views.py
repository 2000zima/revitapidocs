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
from app.utils import get_schema, check_available_years, Timer
from app.utils import process_query, search_db, track_search
from app.gists import get_gists
from app.db import db_json, namespace_jsons

available_apis = app.config['AVAILABLE_APIS']

@cache.cached(timeout=600)
@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    title = 'Revit API Docs'
    return render_template('index.html', title=title)


@cache.cached(timeout=600)
@app.route('/<string:year>/', methods=["GET"])
def api_year_home(year):
    """ Home of api years. Inserts home.html into api.html base"""
    template = 'api.html'

    if year not in available_apis:
        abort(404)

    content_path = 'home.html'
    schema = {
        'title': 'Revit API {}'.format(year),
        'description':
            'Full Online Documentation for Revit API {}'.format(year)}

    return render_template(template, year=year, content=content_path,
                           schema=schema)


@app.route('/<string:year>/<path:filename>', methods=["GET"])
def api_year_file(year, filename):
    """ API Pate. Inserts xxx-xxx.html into api.html base"""
    template = 'api.html'

    if year not in available_apis:
        abort(404)

    content_path = '{year}/{html}'.format(year=year, html=filename)
    available_in = check_available_years(filename)
    if year in available_in:
        schema = get_schema(filename, year=year)
    elif available_in:
        # file exists but not year requested
        template = 'missing.html'
        schema = get_schema(filename, year=available_in[0])
    else:
        # File was not found
        abort(404)

    return render_template(template, year=year, active_href=filename,
                           content=content_path, available_in=available_in,
                           schema=schema)


@cache.cached(timeout=604800)  # 1 Week
@app.route('/<string:year>/namespace.json', methods=['GET'])
def namespace_get(year):
    namespace_json_year = namespace_jsons.get(year)
    if namespace_json_year:
        return jsonify(namespace_json_year)
    else:
        abort(404)


@app.route('/<string:year>/searchapi', methods=['GET'])
def search_api(year):
    MAX_RESULTS = 500
    query = request.args.get('query')

    if not query or query == '0':
        return jsonify({'error': 'Invalid Query Param'})

    query = process_query(query)
    final_query_pat = re.compile(query, re.IGNORECASE)

    logger.debug('Search Query: ' + str(final_query_pat))
    results = search_db(pattern=final_query_pat, field='title')

    if not results: return jsonify({'error': 'No Results'})

    sorted_results = sorted(results, key=lambda k: k['title'])
    if len(sorted_results) > MAX_RESULTS:
        # flash('Results Truncated to 300. Try narrowing your search.')
        sorted_results = sorted_results[:MAX_RESULTS]
    return jsonify(sorted_results)

@app.route('/<string:year>/tracksearch', methods=['GET'])
def track_search_api(year):
    ''' This url received ajax calls from the browser to query+numresults
    and query+clicked to improve Suggestions
    '''
    #/2015/tracksearch?query=XX&numresults=INT
    #/2015/tracksearch?query=XX&clicked=TITLE

    query = request.args.get('query')             # query term
    num_results = request.args.get('numresults')  # number of results
    clicked = request.args.get('clicked')         # name of item/entry
    response, response_json = track_search(query, num_results=num_results, clicked=clicked)
    try:
        return jsonify(response_json)
    except:
        logger.error('Could not jsonify response: {}'.format(response_json))
        return jsonify({'error':'Could not jsonify response'})



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
