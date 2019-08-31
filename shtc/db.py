import sqlite3


class DB:
    def __init__(self):
        self.conct = sqlite3.connect('tags.db')
        self.curs = self.conct.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS tags (id integer PRIMARY KEY, name text UNIQUE, url text, 
        date text, tags text)''')
        self.conct.commit()


    def insert(self, data):
        insert_query = '''INSERT OR REPLACE INTO tags(name, url, date, tags) VALUES (?, ?, ?, ?)'''
        self.curs.execute(insert_query, data)
        self.conct.commit()


    def get(self, name):
        get_query = '''SELECT * FROM tags WHERE name = ?'''
        self.curs.execute(get_query, (name,))

        return self.curs.fetchone()


    def delete(self, name):
        delete_query = '''DELETE FROM tags WHERE name = ?'''
        self.curs.execute(delete_query, (name,))
        self.conct.commit()


    def exist(self, name):
        get_exist_sql = '''SELECT EXISTS(SELECT id FROM tags WHERE name=? LIMIT 1)'''
        self.curs.execute(get_exist_sql, (name,))
        exist = bool(self.curs.fetchone()[0])

        return exist