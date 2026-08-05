"""
QPhotoCleaner
Duplicate Engine
"""

from hashing import calculate_sha256


class DuplicateEngine:

    def __init__(self, db):

        self.db = db

    def calculate_hashes(self):
        """
        サイズが重複しているファイルのみSHA-256を計算する
        """

        rows = self.db.get_duplicate_size_candidates()

        total = len(rows)

        print(f"SHA-256計算対象 : {total} 件")

        for i, row in enumerate(rows, start=1):

            sha256 = calculate_sha256(row["path"])

            self.db.update_sha256(
                row["id"],
                sha256
            )

            if i % 50 == 0 or i == total:
                print(f"{i} / {total}")

        self.db.commit()

        self.db.mark_duplicates()

    def show_duplicates(self):
        """
        重複一覧をコンソールへ表示する
        """

        rows = self.db.get_duplicate_hashes()

        current_group = None

        duplicate_count = 0

        for row in rows:

            group = row["duplicate"]

            if group != current_group:

                current_group = group

                print()
                print("=" * 50)
                print(f"Duplicate Group {group}")
                print("=" * 50)

            print(row["path"])

            duplicate_count += 1

        return duplicate_count