"""
QPhotoCleaner
SHA-256 Hash Engine
Version 1.5.0
"""

import hashlib


def calculate_sha256(filepath, chunk_size=1024 * 1024):
    """
    ファイルのSHA-256を計算する。

    1MBずつ読み込むため、大きな動画でも
    メモリを大量消費しない。
    """

    sha256 = hashlib.sha256()

    try:

        with open(filepath, "rb") as file:

            while True:

                data = file.read(chunk_size)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except (OSError, IOError) as error:

        print(
            f"SHA-256計算失敗: {filepath}"
        )

        print(error)

        return None