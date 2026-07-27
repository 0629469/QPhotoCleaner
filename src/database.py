"""
QPhotoCleaner
SQLite Database
"""

import sqlite3
from pathlib import Path


DB_FILE = Path("database/qphotocleaner.db")


def create_database():

    DB_FILE.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_FILE)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        path TEXT UNIQUE,

        filename TEXT,

        extension TEXT,

        size INTEGER,

        modified REAL,

        media_type TEXT,

        sha256 TEXT

    )
    """)

    conn.commit()

    conn.close()


def get_connection():

    return sqlite3.connect(DB_FILE)