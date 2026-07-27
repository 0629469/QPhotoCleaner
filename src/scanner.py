"""
QPhotoCleaner
Scanner
"""

from pathlib import Path


IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif",
    ".bmp", ".heic", ".tif", ".tiff"
}

VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".avi",
    ".m4v", ".mts", ".m2ts", ".3gp"
}


def scan_folder(folder):

    folder = Path(folder)

    files = []

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        ext = file.suffix.lower()

        if ext in IMAGE_EXTENSIONS:
            media = "image"

        elif ext in VIDEO_EXTENSIONS:
            media = "video"

        else:
            continue

        stat = file.stat()

        files.append({

            "path": str(file),

            "filename": file.name,

            "extension": ext,

            "size": stat.st_size,

            "modified": stat.st_mtime,

            "media_type": media

        })

    return files