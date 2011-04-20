import httplib
import json
import time
import redditdb

_host = 'www.reddit.com'
_headers = {"User-agent" : "rs-v1"}
_retries = 3
_maxscore = 99999999

def _prepareurl(url, after=None):
	tokens = url.split('?')
	if len(tokens) not in (1,2):
		raise Exception( "Improperly formed URL %s", url )
	
	url = tokens[0] + ('.json' if not tokens[0].endswith('.json') else '')
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
		

class RedditScraper:
	def __init__(self, dbname='default.db'):
		self.db = redditdb.RedditDatabase(dbname)
		pass
		
		
	def scrape(self, url='/top/?t=all', pagelimit=-1, scorelimit=-1, delay=1):
		minscore = _maxscore
		after = None
		pagenum = 0
		
		while pagelimit != 0 and minscore > scorelimit:
			pagenum += 1
			url = _prepareurl(url, after)
			print 'Requesting ', _host + url, ' (page %d)...' % pagenum
			res = self._scrapepage(url, pagelimit, scorelimit, delay, _retries)
			
			if res:
				(after, minscore) = res
				pagelimit -= 1
			if not res or not after:
				print 'scrape finished'
				break

		
	def _scrapepage(self, url, pagelimit, scorelimit, delay, tries):
		if tries == 0:
			print 'Failed to scrape %s...' % (_host + url)
			return None
	
		try:
			#connect to Reddit and download JSON page
			conn = httplib.HTTPConnection(_host)
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
			return (after, minscore)
		except Exception as e:
			print 'Reddit Scrapper Error:', e
			print 'retrying %s...' % (_host + url)
			return self._scrapepage(url, pagelimit, scorelimit, delay, tries-1)
			
			
			
	def _parsepage(self, data):
		page = json.loads(data)
		if not page['kind'] == 'Listing':
			return (None, 0)
			
		after = page['data']['after']
		minscore = _maxscore
		
		for child in page['data']['children']:
			if child['kind'] == 't3':
				sub = child['data']
				self.db.writesubmission(sub)
				minscore = min( minscore, int(sub['score']) )
		
		print '    writing %d submissions (minscore = %d) to database...' % (len(page['data']['children']), minscore)
		return (after, minscore)
