# p -m unittest discover -s . -b -v

import os
import unittest
import tempfile
from flask import request
import logging

from app import app
from app.logger import logger
from app.utils import check_available_years, get_schema, create_permutation_query
from app.db import db, db_query

logger.setLevel(logging.ERROR)

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
        r = self.app.get('/static/css/bootstrap.css')
        self.assertEqual(r.status_code, 200)

    def test_robot(self):
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

    def test_check_available_in(self):
        with app.test_request_context('/'):
            rv = check_available_years(self.filename)
            self.assertEqual(rv, ['2015','2016','2017'])

    def test_get_schema(self):
        rv = get_schema(self.filename, '2015')
        self.assertEqual(rv['title'], 'Application Class')
        self.assertEqual(rv['description'], 'Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.')
        self.assertEqual(rv['namespace'], 'Autodesk.Revit.ApplicationServices')

    def test_permitation_query(self):
        query = 'Create Wall'
        perm_query = create_permutation_query(query)
        self.assertEqual('((create).*(wall))|((wall).*(create))', perm_query)

class DbTestCase(unittest.TestCase):

    def setUp(self):
        self.db = db

    def test_href(self):
        rv = self.db.search(db_query.title=='Namespaces')[0]
        self.assertEqual(rv['href'], 'd4648875-d41a-783b-d5f4-638df39ee413.htm')

    def test_title(self):
        rv = self.db.search(db_query.title=='Namespaces')[0]
        print(rv)
        self.assertEqual(rv['title'], 'Namespaces')

    def test_all(self):
        rv = self.db.all()
        self.assertGreater(len(rv), 10000)

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
        assert 'Something went wrong' in str(rv.data)
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()
