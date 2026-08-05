"""
QPhotoCleaner
Folder Scanner
"""

from pathlib import Path


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".webp",
    ".heic",
    ".heif",
    ".raw",
    ".cr2",
    ".cr3",
    ".nef",
    ".arw",
    ".orf",
    ".rw2",
    ".dng",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mts",
    ".m2ts",
    ".wmv",
    ".mkv",
    ".mpg",
    ".mpeg",
    ".3gp",
    ".flv",
    ".webm",
}


def scan_folder(folder):
    """
    指定フォルダ以下を再帰的にスキャンする
    """

    folder = Path(folder)

    files = []

    for path in folder.rglob("*"):

        if not path.is_file():
            continue

        extension = path.suffix.lower()

        if extension in IMAGE_EXTENSIONS:
            media_type = "image"

        elif extension in VIDEO_EXTENSIONS:
            media_type = "video"

        else:
            continue

        stat = path.stat()

        files.append(
            {
                "path": str(path),
                "filename": path.name,
                "extension": extension,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "media_type": media_type,
            }
        )

    return files