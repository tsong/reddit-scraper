import httplib
import json
import time
import redditdb


class RedditScraper:
	_headers = {"User-agent" : "rs-v1"}

	def __init__(self, dbname='default.db'):
		self.db = RedditDatabase(dbname)
		self.headers = _default_headers
		
		
	def scrape(self, url='/top/?t=all', pagelimit=-1, scorelimit=-1, delay=1):
		url = _prepareurl(url)
		self._scrape(url, pagelimit, karmalimit, delay)
		
		
	def _scrape(self, url, pagelimit, scorelimit, delay, tries=3):
		if pagelimit == 0 or tries == 0: 
			return
	
		try:
			#connect to Reddit and download JSON page
			conn = httplib.HTTPConnection('www.reddit.com', 80)
			conn.request('GET', url, headers=_headers)
			resp = conn.getresponse()
			data = resp.read()
			conn.close()
			
			if resp.status != 200:
				raise Exception( 'Bad Response (%d %s)' % (resp.status, resp.reason) )
			
			(after, minscore) = self._parsepage(data)
			if after == None or minscore < scorelimit:
				return
			
			time.sleep(delay)
			
			url = _prepareurl(url, after)
			self._scrape(url, pagelimit-1, scorelimit, delay)

		except Exception as e:
			print 'Reddit Scrapper Error:', e
			print '    retrying... (%d tries remaining)' % (tries-1)
			self._scrape(url, pagelimit, scorelimit, delay, tries-1)
				
	def _prepareurl(url, after=None):
		tokens = url.split('?')
		if len(tokens) not in (1,2):
			raise Exception( "Improperly formed URL %s", url )
		
		url = tokens[0] + '.json'
		query = ''
		if len(tokens) > 1: 
			queries = tokens[1].split('&')
			query += '&'.join([q for q in queries if not q.startswith('after=')])
		if after: 
			if len(query) > 0: 
				query += '&'
			query += 'after=%s' % after
		if len(query) > 0:
			url += '?' + query 
		
		return url
		
			
	def _parsepage(self, data):
		page = json.loads(data)
		if not page['kind'] == 'Listing':
			return (None, 0)
			
		after = page['data']['after']
		minscore = 9999999	#effectively infinity
		
		for child in page['data']['children']:
			if child['kind'] == 't3':
				sub = child['data']
				self.db.writesubmission(sub)
				minscore = min( minscore, int(sub['score']) )
		
		return (after, minscore)
		
