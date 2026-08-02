import sqlite3


class Database:
    def __init__(self, path="qphotocleaner.db"):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def create(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            path TEXT,
            hash TEXT
        )
        """)
        self.conn.commit()

    def insert(self, path, hash_value=None):
        self.cur.execute("INSERT INTO files(path, hash) VALUES(?, ?)", (path, hash_value))
        self.conn.commit()

    def close(self):
        self.conn.close()
