import os.path
import sqlite3


text = 'TEXT'
integer = 'INTEGER'
real = 'REAL'
boolean = 'BOOLEAN'
tablecolumns = {'domain' : text,
				'subreddit' : text,
				'selftext_html' : text,
				'selftext' : text,
				'author' : text,
			  	'score' : integer,
			  	'over_18' : boolean,
			  	'thumbnail' : text,
			  	'subreddit_id' : text,
			  	'downs' : integer,
			  	'is_self' : booean,
			  	'permalink' : text,
			  	'name' : text,
			  	'created' : real,
			  	'url' : text,
			  	'title' : text,
			  	'created_utc' : real,
			  	'num_comments' : integer,
			  	'ups' : integer}


TABLE_CREATE_SQL = '''
CREATE TABLE submissions
(
domain type,
media_embed type,
levenshtein type,
subreddit type,
selftext_html type,


)
'''



class RedditDatabase:
	def __init__(self, dbname='default.db'):
		isfile = os.path.isfile(dbname)
		self.conn = sqlite3.connect(dbname)
		if not isfile:
			self._inittables()
		
		
	def writesubmission(self, sub):
		c = self.conn.cursor()
		c.execute('''INSERT INTO submissions VALUES ( ''')
		conn.commit()
		c.close()
		
	def query(self, sql):
		c = self.conn.cursor()
		c.execute(sql)
		return c
		
	def _inittables():
		c = self.conn.getcursor()
		conn.commit()
		c.close()
