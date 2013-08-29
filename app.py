import os
from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util

MONGOHQ = os.environ['MONGOHQ']
db = MongoClient(MONGOHQ)['issues_io']['repos']
app = Flask(__name__)

@app.route('/')
def index():
    num_repos = db.find().count()
    db_languages = db.aggregate([ {
        "$group": {
            "_id": {
                "language": "$language",
            },
            "num_repos": {
                "$sum": 1,
            },
            "num_issues": {
                "$sum": "$open_issues"
            }
        }},
        {"$sort": {"num_repos": -1}
    } ])

    top_languages = db_languages['result'][0:6]
    remaining = db_languages['result'][6:]
    remaining.sort(key=lambda l: l["_id"]["language"])

    languages = []
    num_issues = 0
    for l in top_languages + remaining:
        lang = l["_id"]["language"]
        if lang is not None:
            languages.append(lang)
            num_issues += l["num_issues"]
        else:
            languages.append("")

    return render_template('index.html', num_repos=num_repos, num_issues=num_issues,
                            languages=languages)

@app.route('/languages')
def getLanguages():
	languages = db.distinct('language')
	for i in range(len(languages)):
		if languages[i] is None:
			languages.pop(i)
			break

	return json_util.dumps(languages)

@app.route('/issues/<language>')
def getIssues(language):
    issues = db.find({'language':language}).sort('open_issues', -1)
    count = db.find({'language':language}).count()
    doc = {
        'count': count,
        'issues': issues
    }
    return json_util.dumps(doc)

