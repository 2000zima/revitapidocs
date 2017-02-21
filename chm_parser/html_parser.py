""" Main Soup Parser

The main functions of this parser is:
1. Remove unecessary markup from html page (_remove_junk_from_soup)
2. Extract "entry" data from html page so DB.json ca be created (get_entry_data_from_soup)
#2 above returns a dictionary for each page processed. Those dictionaries are use
as the first pass in creating the db_index.json

Secondary:
3. Inject Title Header
4. Inject testing tags
5. Extract final clean div
6. Perform batch replacements

db_index.json output:

{
 "00feb0be-205e-2c2d-abdf-939d3a672fb5.htm": {
  "member_of": "Autodesk.Revit.DB.BuiltInFailures.InfillFailures",
  "type": "entry",
  "href": "00feb0be-205e-2c2d-abdf-939d3a672fb5.htm",
  "namespace": "Autodesk.Revit.DB",
  "member_of_href": "13a26a89-322c-ef1a-f5f1-8cd481ee4ba0.htm",
  "description": "Could not change type due to highlighted infilling element. 'Sloped glazing' infills are not allowed.",
  "title": "InfillNoSlopeGlazing Property",
  "tag": "Property"
 },
 "004fe9d1-0b32-4ed3-b8c6-42e0ae00a5a3.htm": {
  "member_of": "Autodesk.Revit.DB.ExtensibleStorage",
  "type": "entry",
  "href": "004fe9d1-0b32-4ed3-b8c6-42e0ae00a5a3.htm",
  "namespace": "Autodesk.Revit.DB.ExtensibleStorage",
  "member_of_href": "81cb1798-3dbe-658b-5a04-d97aa2cb4de9.htm",
  "description": "",
  "title": "ExtensibleStorageFilter Members",
  "tag": "Members"

PS: type: entry means the "entry" has it's own page.

 """

import os
import re
from bs4 import BeautifulSoup
from docopt import docopt

from logger import logger
from .config import TAGS, TEST_CSS_PATH, STATIC_ASSET_EXPRESSION
from .config import AUTODESK_NAMESPACE


def parse_soup(raw_soup, filename, testing=True):
    """ Main Function for Soup Parser """
    entry = get_entry_data_from_soup(raw_soup, filename)
    clean_soup = _remove_junk_from_soup(raw_soup)
    if testing:
        final_soup = _inject_title(clean_soup, entry)
        return _inject_testing_tags(final_soup), entry
    return _final_div_from_body(clean_soup), entry


def make_soup(html_content):
    """ Makes soup object from html_content """
    soup = BeautifulSoup(html_content, 'html5lib')  # utf-8-sig
    # soup = BeautifulSoup(html_content, 'html.parser') # utf8
    return soup


def get_entry_data_from_soup(soup, filename):
    """ Extracts all data from a soup for member entry database.
      {
      "type":"entry",
      "member_of_href":"6f2d8dc7-6a19-fba3-00ae-a88cfe0e3d34.htm",
      "description":"Returns true if the properties CreatedPhaseId and DemolishedPhaseId can be modified for this Element.",
      "title":"CutMarkType Members",
      "member_of":"CutMarkType Class",
      "namespace":"Autodesk.Revit.DB.Architecture",
      "tag":"Members",
      "href":"d854e0db-0621-3288-82b0-1be4b9976a0d.htm"
      }

      type > entry: extracted from an html file. A Full entry (Wall Class)
      type > member: extracted from member list. Does not have its own page  a BIP Parameter

      member_of: Parent entry
      member_of_href: href (html filename) of parent
      title: title of entry
      namespace: main namespace, ie DB
      tag:

    """

    entry = {}

    # href is filename
    entry['href'] = filename

    # Type is entry if it has a page
    entry['type'] = 'entry'

    ###################
    # Get Title       #
    ###################
    entry['title'] = soup.title.text.strip()
    entry['short_title'] = entry['title'].split(' ')[0]

    ##################
    # Get TAG        #
    ##################
    for tag in TAGS:
        if tag.lower() in entry['title'].lower():
            break
    else:
        logger.error('No Tag Found: {}'.format(entry['href']))
        import pdb; pdb.set_trace()

    entry['tag'] = tag

    #####################
    # Namespace Return  #
    #####################
    if 'Namespace' in entry['title']:
        entry['type'] = 'namespace'
        entry['description'] = ''
        entry['tag'] = 'Namespace'
        entry['member_of'] = 'Namespace'
        entry['namespace'] = 'Namespace'
        entry['member_of_href'] = AUTODESK_NAMESPACE
        return entry

    ##################
    # Get namespace  #
    ##################
    # <meta content="Autodesk.Revit.DB.Mechanical" name="container"/>
    namespace = soup.find('meta', {'name': 'container'})
    if namespace and namespace['content'].lower() != 'unknown':
        entry['namespace'] = namespace['content']
    else:
        logger.error('Namespace not Found: {}'.format(entry['href']))
        import pdb; pdb.set_trace()

    ###################
    # Get description #
    ###################
    abstract = soup.find('mshelp:attr', {'name': 'Abstract'})
    if abstract:
        entry['description'] = clean_string(abstract['value'])
    else:
        entry['description'] = ''

    ###################
    # Parent Class    #
    ###################

    # <meta name="Microsoft.Help.Id" content="P:Autodesk.Revit.DB.Electrical.ElectricalDemandFactorValue.MaxRange" />
    # Extract namespace path from Help Id. Removes X:
    microsoft_id = soup.find('meta', {'name': 'Microsoft.Help.Id'})['content']
    # pat = re.compile(r'(?:\:)(?P<member_of>[\w\.]+)')
    # Autodesk.Revit.DB.SATExportOptions.#cto
    pat = re.compile(r'(?:\:)(?P<member_of>(\w|(\.\w))+)')
    match = re.search(pat, microsoft_id)
    original_member_of = match.group('member_of')
    # member_of = Autodesk.Revit.DB.Electrical.ElectricalDemandFactorValue.MaxRange

    # Excludes self from namespace path: Check if last 'chunk is in title'
    # Autodesk.Revit.DB.Electrical.ElectricalDemandFactorValue.MaxRange >
    # Autodesk.Revit.DB.Electrical.ElectricalDemandFactorValue
    member_of_chunks = original_member_of.split('.')

    title_wout_type = entry['title'].split(' ')[0]
    # MaxRange Property > Max Range
    # BuiltInFailures.SelectionFailures Class > BuiltInFailures.SelectionFailures

    # Remove self from member_of path: Remove Max Range:
    # member_of_chunks = ['Autodesk' ,'Revit', 'DB', 'Electrical', ElectricalDemandFactorValue' ,'MaxRange']
    # member_of_chunks = ['Autodesk' ,'Revit', 'DB', 'Electrical', ElectricalDemandFactorValue']
    if original_member_of.endswith(title_wout_type):
        member_of_chunks.pop(-1)
        member_of = '.'.join(member_of_chunks)
    else:
        logger.warning('Could not member_of did not end in title. will set to original_member_of. check:')
        member_of = original_member_of
        # 'ExtensibleStorage' was tripping this up.  Handled now, so check if it's not.
        if 'ExtensibleStorage' not in entry['namespace']:
            logger.warning('Could not member_of did not end in title. will set to original_member_of. check:')
            member_of = original_member_of
            import pdb; pdb.set_trace()

    direct_parent = member_of_chunks[-1]
    try:
        potential_parents = soup.find('div', {'id': 'seeAlsoSection'}).find_all('a')
    except:
        logger.warning('No See also section. Verify: {}'.format(filename))
        import pdb; pdb.set_trace()
    else:
        for a_tag in potential_parents:
            if direct_parent in a_tag.text:
                member_of_href = a_tag['href']
                break
        else:
            logger.error('No member_of href name match in See Also. Verify: {}'.format(filename))
            import pdb; pdb.set_trace()

    entry['member_of'] = member_of
    entry['member_of_href'] = member_of_href

    # TODO: Get API Release
    # api_release_p = soup.html.body.find('div', {'class':'summary'}).find_next_sibling('p')
    # if api_release_p:
    #     match = re.search(r'(?:\()(?P<release>[\d\.]*)(?:\))', api_release_p.text)
    #     if match:
    #         entry['api_release'] = match.group('release')

    return entry


def _remove_junk_from_soup(soup):
    """ Removes unwanted html markup from original html.
    This includes <scrip> tags, xml used for CHM reader, input, imgs, extract
    and a lot more.
    """

    # Remove Head
    soup.head.extract()
    # Remove Head
    soup.find('xml').extract()
    # # All script, xml
    [script_tag.extract() for script_tag in soup.find_all('script')]
    [script_tag.extract() for script_tag in soup.find_all('link')]
    # # All Input Tags
    [script_tag.extract() for script_tag in soup.find_all('input')]
    # # All Images directly within Body - Clears Top nav bar images
    # # <img alt="Collapse image" id="collapseImage" src="../icons/collapse_all.gif" style="display:none; height:0; width:0;" title="Collapse image"/>
    [script_tag.extract() for script_tag in soup.body.find_all('img', recursive=False)]
    #
    # # Footer
    [script_tag.extract() for script_tag in soup.find_all('div', {"id": "footer"})]
    #
    # # Replaces Image Path for Dynamo URL
    for img_tag in soup.find_all('img'):
        img_filename = img_tag['src'].split('/')[-1]
        img_tag['src'] = STATIC_ASSET_EXPRESSION.format(img_filename)
    #
    # # Options
    [script_tag.extract() for script_tag in soup.find_all('span', {"id": "memberOptionsDropdown"})]
    [script_tag.extract() for script_tag in soup.find_all('div', {"id": "memberOptionsMenu"})]
    # # Top Table Collpse Options
    soup.find('tr', {"id": "headerTableRow1"}).extract()
    soup.find('tr', {"id": "headerTableRow2"}).extract()
    soup.find('table', {"id": "gradientTable"}).extract()
    #

    # # Removes script calls from this div, which is child of mainBody
    # # <div id="mainSection"><div id="mainBody">
    # # <div class="saveHistory" id="allHistory" onload="loadAll()" onsave="saveAll()">
    script_tag = soup.find('div', {"class": "saveHistory"})
    script_tag.attrs = {}  # Clear attr
    script_tag.attrs['class'] = 'saveHistory'
    # # Feedback Area
    [script_tag.extract() for script_tag in soup.find_all('span', {"class": "feedbackhead"})]
    # # Dev Language
    [script_tag.extract() for script_tag in soup.find_all('span', {"id": "devlangsDropdown"})]
    [script_tag.extract() for script_tag in soup.find_all('div', {"id": "devlangsMenu"})]


    # Remove all but one: 'CS'
    # <span class="languageSpecificText">
    #     <span class="cs">  . </span>
    #     <span class="vb">  . </span>
    #     <span class="cpp">  :: </span>
    #     ...
    # </span>
    for span_tag in soup.find_all('span', {'class': 'languageSpecificText'}):
        if span_tag['class'] != 'cs':
            span_tag.extract()

    # Section  Toggle. Intead of removing, replace with just header.
    # [script_tag.extract() for script_tag in soup.find_all('span', {"onclick": "ExpandCollapseAll(toggleAllImage)"})]
    # <h1 class="heading"><span onclick="ExpandCollapse(syntaxToggle)" style="cursor:default;"
    # onkeypress="ExpandCollapse_CheckKey(syntaxToggle, event)" tabindex="0">
    # <img id="syntaxToggle" class="toggle" name="toggleSwitch" src="../icons/collapse_all.gif">Syntax</span></h1>

    # # Collapsible Code Block
    # [script_tag.parent.extract() for script_tag in soup.find_all('img', {"name": "toggleSwitch"})]
    heading_tags = soup.find_all('h1', {'class':'heading'})
    for script_tag in heading_tags:
        # import pdb; pdb.set_trace()
        new_h1_tag = soup.new_tag("h1")
        new_h1_tag['class'] = 'heading'
        new_h1_tag.append(script_tag.text.strip())
        script_tag.replace_with(new_h1_tag)

    # Removing this broke script OpenSection
    # After headings were replaced, remove remaining Toggle
    [script_tag.extract() for script_tag in soup.find_all('span', {"onclick": "ExpandCollapseAll(toggleAllImage)"})]
    [script_tag.extract() for script_tag in soup.find_all('span', {"onclick": "ExpandCollapse(exampleToggle"})]

    # Formatted Code <pre xml:space="preserve"> >>> <pre><code></code></pre>
    for script_tag in soup.find_all('pre'):
        if script_tag.get('xml:space'):
            new_pre_tag = soup.new_tag("pre")
            new_pre_tag.insert(0, soup.new_tag('code'))
            new_pre_tag.find('code').contents = script_tag.contents
            script_tag.replace_with(new_pre_tag)



    REMOVE_ATTRIBUTES = ['x-lang','onmouseover','onkeypress','onclick','onmouseout', 'onmouseover','tabindex'
                         'cellpadding', 'cellspacing', ]
    # 'script','style','font', 'dir','face','size','color','style','class','width','height','hspace',
    # 'border','valign''text','link','vlink','alink', 'cellpadding','cellspacing','align'
    for tag in soup.recursiveChildGenerator():
        # print(tag)
        # input('continue?')
        try:
            tag.attrs = {key:value for key, value in tag.attrs.items() if key not in REMOVE_ATTRIBUTES}
        except AttributeError:
            # 'NavigableString' object has no attribute 'attrs'
            pass


    return soup


def _inject_title(soup, entry):
    h1_tag = soup.new_tag("h1")
    h1_tag.string = entry['title']
    soup.body.insert(0, h1_tag)
    return soup


def _final_div_from_body(soup):
    """ Inject New Content in Soup and cleans outter divs"""
    # Inject Tile
    final_soup = soup.new_tag('div')
    final_soup['class'] = 'chm_content'
    final_soup.contents = soup.body.contents
    return final_soup


def _inject_testing_tags(soup, css_path=TEST_CSS_PATH):
    """ Re-inserts a <head> tag and a css reference to test files """
    head_tag = soup.new_tag('head')
    style_tag = soup.new_tag('link')
    style_tag['rel'] = 'stylesheet'
    style_tag['href'] = css_path
    head_tag.insert(0, style_tag)
    soup.html.insert(0, head_tag)
    return soup


def batch_replacement(string, replacement_list, force_ignore=False):
    """ Helper to do process replacement tuples, and enforce replacement """
    for replacement in replacement_list:
        old_pattern = re.compile(replacement.old_pattern)
        new_pattern = replacement.new_pattern
        string, was_replaced = re.subn(old_pattern, new_pattern, string)
        if not force_ignore and (replacement.mandatory and not was_replaced):
            raise Exception('Replacement error: could not replace[{}]'.format(replacement))
    return string

def clean_string(string):
    """ Selective replacement, targets "Title" """
    # NO BREAK SPACE
    string = re.sub('\u00a0', ' ', string)
    string = re.sub('\ufeff', '', string)
    # breakline character
    string = re.sub(r'\n', '', string)
    # Multiple spaces
    string = re.sub(r'\s{2,}', ' ', string)
    # BuiltInFailures..::..RegenFailures Class"
    string = string.replace('..::..', '.')
    #  Replaces "something" with 'something' for better json reading
    string = string.replace('"', "'")
    return string
