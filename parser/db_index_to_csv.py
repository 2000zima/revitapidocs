import os
import json
import csv

print(os.getcwd())

db = os.path.join('app', 'templates', 'json', 'db_index.json')

with open(db) as fp:
    jdata = json.load(fp)

lines = []

for i in jdata.values():
    score = 0
    # if 'class' in ['tag'].lower():
        # score += 1
    if ['description'] != '':
        score += 1
    if ['namespace'] == 'Autodesk.Revit.UI' or ['namespace'] == 'Autodesk.Revit.DB':
        score += 1
    description = i['description'].replace(',',';')
    title = i['title'].replace(',',';')
    # line = ','.join([i['title'], str(score),'','',description])
    line = [title, str(score), '', '', description]
    lines.append(line)


OUT = 'db_autocomple.csv'

with open(OUT, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')

    spamwriter.writerows(lines)
