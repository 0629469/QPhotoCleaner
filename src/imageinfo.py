"""
QPhotoCleaner
Image Information
"""

from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


class ImageInfo:

    @staticmethod
    def get(filepath):
        """
        画像情報を取得する

        Returns
        -------
        dict
        """

        info = {

            "width": None,
            "height": None,
            "taken": "",
            "filesize": 0

        }

        try:

            path = Path(filepath)

            info["filesize"] = path.stat().st_size

            with Image.open(filepath) as image:

                info["width"] = image.width
                info["height"] = image.height

                exif = image.getexif()

                if exif:

                    for tag_id, value in exif.items():

                        tag = TAGS.get(tag_id, tag_id)

                        if tag == "DateTimeOriginal":

                            info["taken"] = str(value)

                            break

        except Exception:

            pass

        return info

    @staticmethod
    def format_size(size):

        if size >= 1024 * 1024 * 1024:
            return f"{size / 1024 / 1024 / 1024:.2f} GB"

        if size >= 1024 * 1024:
            return f"{size / 1024 / 1024:.2f} MB"

        if size >= 1024:
            return f"{size / 1024:.2f} KB"

        return f"{size} B"

    @staticmethod
    def format_resolution(width, height):

        if width is None or height is None:
            return ""

        return f"{width} × {height}"