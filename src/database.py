"""
QPhotoCleaner
SQLite Database
"""

import sqlite3
from pathlib import Path

DB_FILE = Path("database/qphotocleaner.db")


class Database:

    def __init__(self):

        DB_FILE.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def create(self):

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS files(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            path TEXT UNIQUE,
            filename TEXT,
            extension TEXT,
            size INTEGER,
            modified REAL,
            media_type TEXT,

            sha256 TEXT,

            duplicate INTEGER DEFAULT 0

        )
        """)

        self.conn.commit()

    def clear(self):

        self.cur.execute("DELETE FROM files")
        self.conn.commit()

    def insert(self, file):

        self.cur.execute("""

        INSERT OR REPLACE INTO files(

            path,
            filename,
            extension,
            size,
            modified,
            media_type,
            sha256

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            file["path"],
            file["filename"],
            file["extension"],
            file["size"],
            file["modified"],
            file["media_type"],
            None

        ))

    def commit(self):

        self.conn.commit()

    def count(self):

        self.cur.execute("SELECT COUNT(*) FROM files")
        return self.cur.fetchone()[0]

    def get_duplicate_size_candidates(self):
        """
        サイズが重複しているファイルを取得
        """

        self.cur.execute("""

            SELECT *

            FROM files

            WHERE size IN (

                SELECT size

                FROM files

                GROUP BY size

                HAVING COUNT(*) > 1

            )

            ORDER BY size

        """)

        return self.cur.fetchall()

    def update_sha256(self, file_id, sha256):
        """
        SHA-256を書き込む
        """

        self.cur.execute(

            """

            UPDATE files

            SET sha256=?

            WHERE id=?

            """,

            (sha256, file_id)

        )

    def get_duplicate_hashes(self):
        """
        SHA-256が一致したファイルを取得
        """

        self.cur.execute("""

            SELECT *

            FROM files

            WHERE sha256 IN (

                SELECT sha256

                FROM files

                WHERE sha256 IS NOT NULL

                GROUP BY sha256

                HAVING COUNT(*) > 1

            )

            ORDER BY sha256

        """)

        return self.cur.fetchall()

    def close(self):

        self.conn.close()