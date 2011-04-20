import os.path
import sqlite3


_text = 'TEXT'
_integer = 'INTEGER'
_real = 'REAL'
_boolean = 'BOOLEAN'
_subcolumns = {'domain' : _text,
				'subreddit' : _text,
				'selftext_html' : _text,
				'selftext' : _text,
				'author' : _text,
			  	'score' : _integer,
			  	'over_18' : _boolean,
			  	'thumbnail' : _text,
			  	'subreddit_id' : _text,
			  	'downs' : _integer,
			  	'is_self' : _boolean,
			  	'permalink' : _text,
			  	'name' : _text,
			  	'created' : _real,
			  	'url' : _text,
			  	'title' : _text,
			  	'created_utc' : _real,
			  	'num_comments' : _integer,
			  	'ups' : _integer}


CREATE_TABLE_SQL = 'CREATE TABLE submissions (%s)' % ', '.join([c + ' ' + str(_subcolumns[c]) for c in _subcolumns.keys()])


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
		c.execute(CREATE_TABLE_SQL)
		conn.commit()
		c.close()
