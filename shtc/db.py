import sqlite3


class DB:
    def __init__(self):
        self.conct = sqlite3.connect('url-data.db')
        self.curs = self.conct.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS url-data (id integer primary key, name text, url text, date text, tags blob)''')
        self.conct.commit()


    def insert_data(self, name, url, date, tags):
        insert_sql = '''INSERT INTO url-data(name, url, date, tags) VALUES (?, ?, ?, ?,)'''
        self.curs.execute(insert_sql, (name, url, date, tags,))
        self.conct.commit()

    def get_data(self, name):
        get_data = '''SELECT * FROM url-data WHERE name = ?'''
        self.curs.execute(get_data, (name,))
        self.conct.commit()


    # def update_data(self, name, date, tags):
    #     self.curs.execute('''UPDATE url-data(name, url, date, tags) VALUES (?, ?, ?, ?)''',
    #                       name, url, date, tags)
    #     self.conct.commit()