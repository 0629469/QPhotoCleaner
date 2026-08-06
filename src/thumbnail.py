"""
QPhotoCleaner
Thumbnail Engine
"""

from PIL import Image
from PIL import ImageTk


class ThumbnailEngine:

    def __init__(self, size=(256, 256)):

        self.size = size

        #
        # Tkinterで画像が消えないように保持する
        #
        self.cache = {}

    def load(self, filepath):
        """
        サムネイルを作成する

        Parameters
        ----------
        filepath : str

        Returns
        -------
        ImageTk.PhotoImage
            読み込み失敗時は None
        """

        #
        # キャッシュ
        #
        if filepath in self.cache:
            return self.cache[filepath]

        try:

            image = Image.open(filepath)

            image.thumbnail(
                self.size,
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(image)

            self.cache[filepath] = photo

            return photo

        except Exception:

            #
            # 読めない画像
            #
            return None

    def clear(self):
        """
        キャッシュをクリア
        """

        self.cache.clear()