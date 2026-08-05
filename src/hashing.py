"""
QPhotoCleaner
SHA-256 Hash Engine
"""

import hashlib


def calculate_sha256(filepath, buffer_size=1024 * 1024):
    """
    ファイルのSHA-256を計算する

    Parameters
    ----------
    filepath : str
        対象ファイル

    buffer_size : int
        読み込みサイズ（デフォルト1MB）

    Returns
    -------
    str
        SHA-256文字列
    """

    sha = hashlib.sha256()

    with open(filepath, "rb") as f:

        while True:

            data = f.read(buffer_size)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()