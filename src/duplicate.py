"""
QPhotoCleaner
Duplicate Engine
Version 1.5.0
"""

from hashing import calculate_sha256


class DuplicateEngine:

    def __init__(self, db):

        self.db = db

    def calculate_hashes(self):
        """
        同一サイズのファイルについてSHA-256を計算する。
        """

        rows = self.db.get_duplicate_size_candidates()

        total = len(rows)

        print(
            f"SHA-256計算対象: {total}件"
        )

        for i, row in enumerate(rows, 1):

            try:

                sha256 = calculate_sha256(
                    row["path"]
                )

                self.db.update_sha256(
                    row["id"],
                    sha256
                )

            except Exception as error:

                print(
                    f"SHA-256計算失敗: "
                    f"{row['path']}"
                )

                print(error)

            if i % 50 == 0 or i == total:

                print(
                    f"{i}/{total}"
                )

        self.db.commit()

        #
        # SHA-256が一致したファイルを
        # 重複グループとしてマーキング
        #

        if hasattr(
            self.db,
            "mark_duplicates"
        ):

            self.db.mark_duplicates()

    def show_duplicates(self):
        """
        完全一致した重複ファイルを表示する。
        """

        rows = self.db.get_duplicate_hashes()

        current_hash = None

        count = 0

        for row in rows:

            sha256 = row["sha256"]

            if sha256 != current_hash:

                current_hash = sha256

                print(
                    f"\n===== Group "
                    f"{row['duplicate']} ====="
                )

            print(
                row["path"]
            )

            count += 1

        return count