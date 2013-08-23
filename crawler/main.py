import requests
from pymongo import MongoClient
from time import sleep
from settings import *

repos = []
github = 'https://api.github.com'

def get_db():
	client = MongoClient('localhost', 27017)
	return client['github']['repos']

def check_ratelimiting():
	while True:
		r = requests.get('https://api.github.com/rate_limit', auth=(USER, PASS))
		body = r.json()
		remaining = body['rate']['remaining']
		if remaining < 100:
			print 'We only have %d requests remaining. Sleeping for 2 mins.' % remaining
			sleep(2*60)
		else:
			print 'We have %d requests remaining so we\'ll continue.' % remaining
			break

def main():
	repos = get_db()
	link = 'https://api.github.com/repositories?since='
	while True:
		check_ratelimiting()
		print 'Downloading:', link
		r = requests.get(link, auth=(USER, PASS))
		for repo in r.json():
			if repo['fork']: continue
			name = repo['full_name']
			repo_link = github + '/repos/' + name
			r2 = requests.get(repo_link, auth=(USER, PASS))
			body = r2.json()
			try:
				open_issues = body['open_issues']
			except:
				continue
			if open_issues >= 10:
				doc = {
					'name':name,
					'language':body['language'],
					'open_issues':open_issues
				}
				prev = repos.find_one(doc)
				if prev != None:
					_id = prev['_id']
					repos.update({'_id':_id}, {"$set": doc}, upsert=False)
					print 'Updated:', doc
				else:
					repos.insert(doc)
					print 'Inserted:', doc
		link = r.headers['link'].split(';')[0].strip('<').strip('>')

if __name__ == "__main__":
	main()