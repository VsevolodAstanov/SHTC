import sys
import sqlite3
from shtc.logger import Logger
from shtc.patterns import Singleton


class DB(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        try:
            self.log = Logger()()
            self.log.info('INITIALIZE SQLite DB')

            self.conct = sqlite3.connect('tags.db')
            self.curs = self.conct.cursor()
            self.curs.execute('''CREATE TABLE IF NOT EXISTS tags (id integer PRIMARY KEY, name text UNIQUE, url text, 
            date text, tags text)''')
            self.conct.commit()
        except:
            self.log.critical('No DB Connection' + str(sys.exc_info()[1]))
            sys.exit()

    def insert(self, data):
        self.log.info('INSERT DATA TO DB')

        insert_query = '''INSERT OR REPLACE INTO tags(name, url, date, tags) VALUES (?, ?, ?, ?)'''
        self.curs.execute(insert_query, data)
        self.conct.commit()

    def get(self, name, url):
        self.log.info('GET DB DATA')

        get_query = '''SELECT name, url, date, tags FROM tags WHERE name = ? AND url = ?'''
        self.curs.execute(get_query, (name, url))

        return self.curs.fetchone()

    def delete(self, name):
        self.log.info('DELETE DB DATA')

        delete_query = '''DELETE FROM tags WHERE name = ?'''
        self.curs.execute(delete_query, (name,))
        self.conct.commit()
