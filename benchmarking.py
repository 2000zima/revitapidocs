# p -m unittest discover -s . -b -v

import os
import unittest
import tempfile
from flask import request
import logging

from app import app
from app.logger import logger
from app.utils import check_available_years, get_schema

# logger.setLevel(logging.ERROR)

class BenchmarkingTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_root(self):


if __name__ == '__main__':
    unittest.main()
