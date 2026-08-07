"""
QPhotoCleaner
Thumbnail Engine
Version 1.4.0
"""

from pathlib import Path

from PIL import Image, ImageTk


class ThumbnailEngine:

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

    def __init__(self, size=(300, 300)):

        self.size = size

    def load(self, filepath):
        """
        指定された画像からサムネイルを作成する。

        読み込みに失敗した場合はNoneを返す。
        """

        path = Path(filepath)

        if not path.exists():
            return None

        try:

            with Image.open(path) as image:

                image = image.convert("RGB")

                image.thumbnail(
                    self.size,
                    Image.Resampling.LANCZOS
                )

                photo = ImageTk.PhotoImage(
                    image.copy()
                )

                return photo

        except Exception as error:

            print(
                f"サムネイルを作成できません: {path}"
            )

            print(error)

            return None

    @staticmethod
    def is_raw(filepath):
        """
        RAW画像か判定する。
        """

        extension = Path(filepath).suffix.lower()

        return extension in ThumbnailEngine.RAW_EXTENSIONS

    @staticmethod
    def is_supported(filepath):
        """
        サムネイル対象の画像か判定する。
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
            ThumbnailEngine.RAW_EXTENSIONS
        )

        extension = Path(filepath).suffix.lower()

        return extension in extensions