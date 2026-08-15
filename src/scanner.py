"""
QPhotoCleaner
File Scanner
Version 1.5.0
"""

from pathlib import Path


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
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

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".mts",
    ".m2ts",
    ".wmv",
    ".flv",
    ".webm",
}


def get_media_type(path):
    """
    拡張子からメディア種別を判定する。
    """

    extension = Path(path).suffix.lower()

    if extension in IMAGE_EXTENSIONS:
        return "image"

    if extension in VIDEO_EXTENSIONS:
        return "video"

    return None


def scan_folder(folder):
    """
    フォルダを再帰的にスキャンする。

    対象:
        image
        video

    QNAP上の共有フォルダを
    Windowsからネットワークドライブや
    UNCパスとして指定して使用できる。
    """

    results = []

    root = Path(folder)

    if not root.exists():
        return results

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        media_type = get_media_type(path)

        if media_type is None:
            continue

        try:

            stat = path.stat()

            results.append({

                "path": str(path),

                "filename": path.name,

                "extension": path.suffix.lower(),

                "size": stat.st_size,

                "modified": stat.st_mtime,

                "media_type": media_type,

            })

        except OSError as error:

            print(
                f"[SKIP] ファイル情報取得失敗: "
                f"{path}"
            )

            print(error)

            continue

    return results