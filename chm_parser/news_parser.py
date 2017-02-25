""" Remove formatting from whats new file

"""

import os
from collections import defaultdict
from pprint import pprint
import difflib

from logger import logger

from .utils import open_html, load_json
from .html_parser import parse_soup, make_soup
from .config import YEARS, DEAFULT_DB_INDEX_MEMBERS_JSON


def parse_news(whatsnew_html_path):
    """ Removes all styling from What's new html file """
    news_html = open_html(whatsnew_html_path)
    print('Making Soup...')
    soup = make_soup(news_html)
    soup.head.style.extract()
    print('Parsing Soup...')
    for tag in soup.recursiveChildGenerator():
        for tag in soup.recursiveChildGenerator():
            try:
                tag.attrs = {key:value for key, value in tag.attrs.items() if key != 'style'}
            except AttributeError:
                # 'NavigableString' object has no attribute 'attrs'
                pass

    final_soup = soup.new_tag('section')
    final_soup['id'] = 'api-content'
    final_soup.contents = soup.body.contents
    return final_soup
