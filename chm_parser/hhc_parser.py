""" HHC parser > Creates Treeview Namespace json

HHC is an html file with a DEEPLY NESTED unordered lists.

the HCC file contains the hierarchical tree-like namespace view
and corresponds to the "CONTENTS" tab of the chm helpfile.

This script helps clean this html structure and convert it into
an equivalent json file that is used by the treeview bootstrap js

The output of this parsing is usually labeled `ns_201X.json`
as the json becomes the namespace tree used in the treeview navigation.

Structure:
- Namespaces
-- Autodesk.Revit.Application
--- Application Class
---- ...
--- Controlled Application Class
---- ...
--- Language Type Enumeration
--- Product Type Enumeration
--- Autodesk.Revit.Attributes
---- ...
--- Autodesk.Revit.Creation
---- ...
    [...]

IN:
<HTML>
<BODY>

<UL>
<LI><OBJECT type="text/sitemap">
  <param name="Name" value="Namespaces">
  <param name="Local" value="html/d4648875-d41a-783b-d5f4-638df39ee413.htm">
</OBJECT></LI>
<UL>
  <LI><OBJECT type="text/sitemap">
    <param name="Name" value="Autodesk.Revit.ApplicationServices Namespace">
    <param name="Local" value="html/91957e18-2935-006c-83ab-3b5b9dbb5928.htm">
  </OBJECT></LI>
  <UL>

OUT:
[
 {
  "text": "Namespaces",
  "href": "html/d4648875-d41a-783b-d5f4-638df39ee413.htm",
  "nodes": [
   {
    "text": "Autodesk.Revit.ApplicationServices Namespace",
    "href": "html/91957e18-2935-006c-83ab-3b5b9dbb5928.htm",
    "nodes": [
     {
      "text": "Application Class",
      "href": "html/94db8ea8-d2c3-5e71-8030-466bcb8e4426.htm",
      "nodes": [
       {
        "text": "Application Members",
        "href": "html/e34107f5-ef2d-ab52-1d17-98a235ca7e10.htm"
       },

"""

from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json


def _dictify(ul):
    """ Recursivively convert nested <li> into dictionary """
    entry = OrderedDict()
    li = ul.find("li")
    param_name = li.find('param', {'name': 'Name'})
    param_href = li.find('param', {'name': 'Local'})

    entry['text'] = param_name['value'].strip()
    html_value = param_href['value'].strip()
    entry['href'] = html_value.replace('html/','')

    nodes = [_dictify(ul_child) for ul_child in ul.find_all("ul", recursive=False)]
    # Adds nodes only to elements w/child
    if nodes:
        entry['nodes'] = nodes

    # Uncomment to make it non-selectable
    # entry['selectable'] = False

    return entry


def parse_namespace(hhc_data, minify=True):
    """ Parses HHC file """
    print('Loading HHC File')
    soup = BeautifulSoup(hhc_data, 'html.parser')
    # soup = BeautifulSoup(content, 'html5lib')
    print('Soup created. Parsing...')

    ul = soup.body.ul
    dicified_hcc = [_dictify(ul)]
    print('Parsing Completed.')

    return dicified_hcc
