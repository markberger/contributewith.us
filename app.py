from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util
from settings import *

db = MongoClient(MONGOHQ)['issues_io']['repos']
app = Flask(__name__)

@app.route('/')
def index():
    languages = db.distinct('language')
    for i in range(len(languages)):
        if languages[i] is None:
            languages.pop(i)
            break
    num_repos = db.find().count()
    num_issues = db.aggregate([ {
    	"$group": {
    		"_id": "null",
    		"total": {
    			"$sum": "$open_issues"
    		}
    	}
    }])
    num_issues = num_issues['result'][0]['total']
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

