# Create Namespace File - Treeview JSON - hhc
`python -m chm_parser parse_namespaces 2015 chm_parser\data\in_2015\RevitAPI.hhc`
`python -m chm_parser parse_namespaces 2016 chm_parser\data\in_2016\RevitAPI.hhc`
`python -m chm_parser parse_namespaces 2017 chm_parser\data\in_2017\RevitAPI.hhc`
`python -m chm_parser parse_namespaces 2017 chm_parser\data\in_2017.1\RevitAPI.hhc`

> test
`python -m chm_parser parse_pages 2016 chm_parser\data\in_2016\html\ --output=app\templates\api_docs\2016\ --single-html=29a6e040-a36e-2a0c-5339-c69aa7776301.htm`
> This creates the JSON needed to build the tree view menu navigation


# Parse Pages - The actual Content + Base Index - html
`python -m chm_parser parse_pages 2015 chm_parser\data\in_2015\html\`
`python -m chm_parser parse_pages 2016 chm_parser\data\in_2016\html\`
`python -m chm_parser parse_pages 2017 chm_parser\data\in_2017\html\`
`python -m chm_parser parse_pages 2017.1 chm_parser\data\in_2017.1\html\`


> Outputs htmls pages and db_index
See html_parser.py for more details

# Parse Members - The Final Index - hhk
* Requires completed Pages
`python -m chm_parser parse_members 2015 chm_parser\data\in_2015\RevitAPI.hhk chm_parser\data\out_2015\html chm_parser\data\out_2015\db_index_2015.json &&
python -m chm_parser parse_members 2016 chm_parser\data\in_2016\RevitAPI.hhk chm_parser\data\out_2016\html chm_parser\data\out_2016\db_index_2016.json &&
python -m chm_parser parse_members 2017 chm_parser\data\in_2017\RevitAPI.hhk chm_parser\data\out_2017\html chm_parser\data\out_2017\db_index_2017.json &&
python -m chm_parser parse_members 2017.1 chm_parser\data\in_2017.1\RevitAPI.hhk chm_parser\data\out_2017.1\html chm_parser\data\out_2017.1\db_index_2017.1.json`

> Outputs db_index_members. Scrapes hhk enumeration members, and gets description from each corresponding page

# Merge - The Final Final Index
* Requires Parse Members and Updated Pages, but they are not dependent
`python -m chm_parser merge chm_parser\data\out_2015\`

> Outputs Merged/db_index.json

# Bootstrap - Combine only required HTML files
* Will Consolidate Pages HTML
`python -m chm_parser bootstrap chm_parser\data\ chm_parser\data\out_Merged\db_index.json chm_parser\data\out_Merged\`


# Parse News
> Cleans up styling from what's new file
> Combined command
`python -m chm_parser parse_news 2015 chm_parser\data\in_2015\WhatsNew.htm --output=chm_parser\data  &&
python -m chm_parser parse_news 2016 chm_parser\data\in_2016\WhatsNew.htm --output=chm_parser\data  &&
python -m chm_parser parse_news 2017 chm_parser\data\in_2017\WhatsNew.htm --output=chm_parser\data &&  
python -m chm_parser parse_news 2017.1 chm_parser\data\in_2017.1\WhatsNew.htm --output=chm_parser\data`


# Folder Structure

* data
** in_2015
*** html
*** RevitAPI.hhc
*** RevitAPI.hhk
** in_2016
***
** out_2016
**** html
**** db_index_2015.json
**** db_members_2015.json
**** namespace_2015.json

** out_2016
