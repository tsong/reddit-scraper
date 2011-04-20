import os.path
import sqlite3


_text = 'TEXT'
_integer = 'INTEGER'
_real = 'REAL'
_boolean = 'BOOLEAN'
_columntypes = {'domain' : _text,
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

_columns = _columntypes.keys()
_primarykey = 'permalink'

CREATE_TABLE_SQL = 'CREATE TABLE submissions (%s, PRIMARY KEY (%s))'\
				   % (', '.join([c + ' ' + str(_columntypes[c]) for c in _columns]), _primarykey)
INSERT_SQL = 'INSERT INTO submissions (%s) VALUES (%s)' % ( ', '.join(_columns), ', '.join('?'*len(_columns)) )



class RedditDatabase:
	def __init__(self, dbname='default.db'):
		isfile = os.path.isfile(dbname)
		self.conn = sqlite3.connect(dbname)
		if not isfile:
			self._inittables()
		
	def writesubmission(self, sub):
		row = tuple( [ sub[c] if c in sub.keys() else None for c in _columns ] )
		pk = sub[_primarykey] if _primarykey in sub.keys() else None
		if not pk: 
			return
			
		#write row to 'submissions' table
		cursor = self.conn.cursor()
		try:
			cursor.execute(INSERT_SQL, row)
		except sqlite3.IntegrityError:
			print 'Reddit database: %s is already in database' % str(pk)
		else:
			self.conn.commit()
			cursor.close()
			
		
	def query(self, sql):
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor
		
	def _inittables(self):
		cursor = self.conn.cursor()
		cursor.execute(CREATE_TABLE_SQL)
		self.conn.commit()
		cursor.close()
