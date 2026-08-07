"""
QPhotoCleaner
Image Information Engine
Version 1.4.0
"""

from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS


class ImageInfo:

    RAW_EXTENSIONS = {
        ".cr2",
        ".cr3",
        ".nef",
        ".arw",
        ".dng",
        ".orf",
        ".rw2",
        ".raf",
        ".srw",
    }

    @staticmethod
    def get(filepath):
        """
        画像情報を取得する

        RAWを含め、読み込みに失敗しても
        QPhotoCleaner全体を停止させない。
        """

        path = Path(filepath)

        result = {
            "width": 0,
            "height": 0,
            "taken": "不明",
            "filesize": 0,
        }

        try:

            if path.exists():
                result["filesize"] = path.stat().st_size

            with Image.open(path) as image:

                result["width"] = image.width
                result["height"] = image.height

                exif = image.getexif()

                if exif:

                    taken = (
                        exif.get(36867)
                        or exif.get(306)
                    )

                    if taken:
                        result["taken"] = str(taken)

        except Exception as error:

            print(
                f"画像情報を取得できません: {path}"
            )

            print(error)

            #
            # RAWなどPillowで読めない場合も
            # アプリケーションを停止しない
            #

            result["taken"] = "情報取得不可"

        return result

    @staticmethod
    def format_resolution(width, height):
        """
        解像度を表示用文字列へ変換
        """

        if not width or not height:
            return "不明"

        return f"{width} × {height}"

    @staticmethod
    def format_size(filesize):
        """
        ファイルサイズを表示用文字列へ変換
        """

        if filesize is None:
            return "不明"

        if filesize < 1024:
            return f"{filesize} B"

        if filesize < 1024 * 1024:
            return f"{filesize / 1024:.1f} KB"

        if filesize < 1024 * 1024 * 1024:
            return f"{filesize / 1024 / 1024:.2f} MB"

        return f"{filesize / 1024 / 1024 / 1024:.2f} GB"

    @staticmethod
    def is_raw(filepath):
        """
        RAW画像か判定する
        """

        extension = Path(filepath).suffix.lower()

        return extension in ImageInfo.RAW_EXTENSIONS

    @staticmethod
    def is_supported_image(filepath):
        """
        QPhotoCleanerで画像として扱う拡張子か判定する
        """

        extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tif",
            ".tiff",
            ".webp",
        }

        extensions.update(
            ImageInfo.RAW_EXTENSIONS
        )

        extension = Path(filepath).suffix.lower()

        return extension in extensions