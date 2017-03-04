# p -m unittest discover -s . -b -v

import os
import unittest
import tempfile
from flask import request
import logging

from app import app
from app.utils.logger import logger
from app.utils.db_utils import get_entry, get_best_entry_match
from app.utils.db import db_json

logger.setLevel(logging.ERROR)

# TODO: Write complete test suite: Search, query_process, priority_list, etc

class UrlsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)

    def test_api(self):
        r = self.app.get('/2015/')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2016/')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2017/')
        self.assertEqual(r.status_code, 200)

    def test_api_content(self):
        r = self.app.get('/2016/ded320da-058a-4edd-0418-0582389559a7.htm')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2016/ded320da-058a-4edd-0418-0582389559a7.htm')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/2016/ded320da-058a-4edd-0418-0582389559a7.htm')
        self.assertEqual(r.status_code, 200)

    def test_static(self):
        r = self.app.get('/static/css/_yeti.scss')
        self.assertEqual(r.status_code, 200)

    def test_robot(self):
        # Need to add test for dev/production
        r = self.app.get('/robot.txt')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r.mimetype, 'text/html')

    def test_site_map(self):
        rv = self.app.get('/sitemap.xml')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.mimetype, 'application/xml')


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = "94db8ea8-d2c3-5e71-8030-466bcb8e4426.htm"
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_entry(self):
        filename = "94db8ea8-d2c3-5e71-8030-466bcb8e4426.htm"
        rv = get_entry(filename)
        self.assertIsInstance(rv, dict)
        self.assertEqual(rv['title'], 'Application Class')
        self.assertEqual(rv['description'], 'Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.')
        self.assertEqual(rv['namespace'], 'Autodesk.Revit.ApplicationServices')

    def test_get_best_entry_match1(self):
        years = {'years':{'2015': 'exists', '2016': 'unchanged', '2017': 'unchanged', '2017.1': 'unchanged'}}
        self.assertEqual(get_best_entry_match(years, '2015'), '2015')
        self.assertEqual(get_best_entry_match(years, '2016'), '2015')
        self.assertEqual(get_best_entry_match(years, '2017'), '2015')
        self.assertEqual(get_best_entry_match(years, '2017.1'), '2015')

    def test_get_best_entry_match2(self):
        years = {'years':{'2015': 'exists', '2016': 'updated', '2017': 'unchanged', '2017.1': 'unchanged'}}
        self.assertEqual(get_best_entry_match(years, '2015'), '2015')
        self.assertEqual(get_best_entry_match(years, '2016'), '2016')
        self.assertEqual(get_best_entry_match(years, '2017'), '2016')
        self.assertEqual(get_best_entry_match(years, '2017.1'), '2016')


    def test_get_best_entry_match3(self):
        years = {'years':{'2015': 'exists', '2016': 'unchanged', '2017': 'updated', '2017.1': 'updated'}}
        self.assertEqual(get_best_entry_match(years, '2015'), '2015')
        self.assertEqual(get_best_entry_match(years, '2016'), '2015')
        self.assertEqual(get_best_entry_match(years, '2017'), '2017')
        self.assertEqual(get_best_entry_match(years, '2017.1'), '2017.1')

    def test_get_best_entry_match4(self):
        years = {'years':{'2016': 'exists', '2017': 'unchanged', '2017.1': 'updated'}}
        self.assertIsNone(get_best_entry_match(years, '2015'))
        self.assertEqual(get_best_entry_match(years, '2016'), '2016')
        self.assertEqual(get_best_entry_match(years, '2017'), '2016')
        self.assertEqual(get_best_entry_match(years, '2017.1'), '2017.1')

    def test_get_best_entry_match5(self):
        years = {'years':{'2015': 'exists', '2016': 'unchanged', '2017': 'unchanged', '2017.1': 'updated'}}
        self.assertEqual(get_best_entry_match(years, '2015'), '2015')
        self.assertEqual(get_best_entry_match(years, '2016'), '2015')
        self.assertEqual(get_best_entry_match(years, '2017'), '2015')
        self.assertEqual(get_best_entry_match(years, '2017.1'), '2017.1')


class HtmlContentCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_python(self):
        rv = self.app.get('/python/')
        assert 'Python' in str(rv.data)

    def test_home(self):
        rv = self.app.get('/2015/')
        # import ipdb; ipdb.set_trace()
        assert 'Revit API 2015' in str(rv.data)
        rv = self.app.get('/2016/')
        assert 'Revit API 2016' in str(rv.data)
        rv = self.app.get('/2017/')
        assert 'Revit API 2017' in str(rv.data)

    def test_404(self):
        rv = self.app.get('/2015/asdasd')
        assert 'Something Went Wrong' in str(rv.data)
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()
