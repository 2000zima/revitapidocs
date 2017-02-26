""" HHC parser > Harvest non-entry members

HHK is an html file with FLAT unordered lists

The HHK file contains a flat list of a all members, and correspond to the
"INDEX" tab in the the helpfile.

The member file is challenging because it duplicates many of the main
entries, and most of it is links to sections of main entries.

The approach I took is to use on certain categories that are more likely
to me usedful.

Structure:
- AA_Gravity enumeration member: html/c273e69a-8851-6f15-dc90-2385359e3c45.htm
- AA_GravityLateral enumeration member": html/c273e69a-8851-6f15-dc90-2385359e3c45.htm
[...]

IN:
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML/EN">
<HTML>
  <BODY>
    <UL>
      <LI><OBJECT type="text/sitemap">
        <param name="Name" value="AA_Gravity enumeration member">
        <param name="Local" value="html/c273e69a-8851-6f15-dc90-2385359e3c45.htm">
      </OBJECT><LI>
      <LI><OBJECT type="text/sitemap">
        <param name="Name" value="AA_GravityLateral enumeration member">
        <param name="Local" value="html/c273e69a-8851-6f15-dc90-2385359e3c45.htm">
      </OBJECT><LI>
      <LI><OBJECT type="text/sitemap">
        <param name="Name" value="AA_Hanger enumeration member">
        <param name="Local" value="html/c273e69a-8851-6f15-dc90-2385359e3c45.htm">

OUT:



"""

from bs4 import BeautifulSoup
from collections import OrderedDict, namedtuple
import re
import os
import sys
from pprint import pprint
import time
import pickle

from logger import logger
from .utils import open_html
from .config import TAGS
from .html_parser import get_entry_data_from_soup, make_soup, clean_string


def _manuallly_parse(hhk_data):
    """ Manually Parses HKK file.
    Substantially faster then BS4, which was also giving errors
    """
    print('Parsing new Soup from HHK File')
    # soup = BeautifulSoup(hhk_data, 'html.parser') # Recursion error w parser
    members = []
    member = {}
    title_pat = re.compile(r'(?:value=")(?P<title>.+)(?:">)')
    href_pat = re.compile(r'(?:value="html/)(?P<href>.+)(?:">)')

    lines = hhk_data.split('\n')
    for line in lines:
        if '<param name' not in line:
            continue
        if '<param name="Name' in line:
            assert member.get('title') is None
            member['title'] = re.search(title_pat, line).group('title')
        elif '<param name="Local' in line:
            assert member.get('title') is not None
            assert member.get('href') is None
            member['href'] = re.search(href_pat, line).group('href')
            members.append(member)
            member = {}
    return members


def parse_members(hhk_data, db_index):
    """ Parses HHK file """
    members = _manuallly_parse(hhk_data)
    members_index = {}

    for member in members:
        member_title = member['title']
        member_href = member['href']

        entry = db_index[member_href]

        pat = re.compile('enumeration member', flags=re.IGNORECASE)
        match = re.search(pat, member_title)
        if not match:
            continue

        corrected_member_title, was_replaced = re.subn('enumeration member', 'Enumeration Member', member_title)
        if not was_replaced:
            logger.warning('Could not fix case. Verify')
            import pdb; pdb.set_trace()

        member = {}
        member['tag'] = 'Enumeration Member'
        member['title'] = corrected_member_title
        member['short_title'] = corrected_member_title.split(' ')[0]
        member['href'] = member_href
        member['member_of_href'] = member_href
        member['member_of'] = '.'.join([entry['member_of'], entry['title']])
        member['type'] = 'member'
        member['namespace'] = entry['namespace']
        member['description'] = ''  # TODO: Open Page, and extract Enum Name
        short_title = corrected_member_title.split(' ')[0]  # TODO: Add to Main ?

        member_key = '{}::{}'.format(member['href'], short_title)
        members_index[member_key] = member
        # print(member['member_of'])

    print('Done Parsing HHK')
    return members_index


def extract_enumeration_descriptions(members_index, in_html_dir):
    """
    Opens all files mentioned my enum members, extracts Description,
    and adds back to enum memer.

    <tr class="selected-enumeration">
      <td target="F:Autodesk.Revit.UI.PostableCommand.StatusBarDesignOptions">
        <span class="selflink">StatusBarDesignOptions</span>
      </td>
      <td>Displays the active design option in the status bar.
      </td>
    </tr>
    """
    print('Extracting Description: {}'.format(len(members_index)))

    # Iterate over needed files only to minimize file opening and parsing.
    unique_html = set([key.split('::')[0] for key in members_index.keys()])

    for filename in unique_html:
        logger.info('Extracting Enum Description: {}'.format(filename))
        html_path = os.path.join(in_html_dir, filename)
        html_content = open_html(html_path)
        soup = make_soup(html_content)

        # Find all enum tags in the page
        enum_span_tags = soup.find_all('span', {'class': 'selflink'})
        for enum_tag in enum_span_tags:
            enum_tag_text = enum_tag.text.strip()
            member_key = '::'.join([filename, enum_tag_text])

            member = members_index.get(member_key)
            if not member:
                logger.warning('No Match Tag. Verify.')
                import pdb; pdb.set_trace()
            else:
                description_tag = enum_tag.parent.find_next_sibling('td')
                if description_tag:
                    description = description_tag.text.strip()
                    member['description'] = clean_string(description)
                    # print('Found Tag: {}:{}'.format(member['short_title'], description.encode('utf-8')))
                else:
                    logger.warning('No Description tag found. Verify')
                    import pdb; pdb.set_trace()

    return members_index
