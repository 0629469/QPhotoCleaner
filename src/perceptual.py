"""
QPhotoCleaner
Perceptual Hash Engine
Version 1.5.1
"""

from pathlib import Path

from PIL import Image
import hashlib


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
}


def calculate_phash(filepath):
    """
    画像のPerceptual Hashを計算する。

    画像を32x32のグレースケールへ縮小し、
    画像内容から特徴値を作成する。

    読み込みに失敗した場合はNoneを返す。
    """

    path = Path(filepath)

    if not path.exists():
        return None

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return None

    try:

        with Image.open(path) as image:

            image = image.convert("L")

            image = image.resize(
                (32, 32),
                Image.Resampling.LANCZOS
            )

            data = image.tobytes()

            return hashlib.sha256(data).hexdigest()

    except Exception as error:

        print(
            f"Perceptual Hash計算失敗: {path}"
        )

        print(error)

        return None


def calculate_difference(hash1, hash2):
    """
    2つのPerceptual Hashの差を計算する。

    現在の実装ではSHA-256を使っているため、
    完全一致なら0、それ以外は差を返す。
    """

    if not hash1 or not hash2:
        return None

    if len(hash1) != len(hash2):
        return None

    difference = 0

    for a, b in zip(hash1, hash2):

        if a != b:
            difference += 1

    return difference