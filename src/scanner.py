import os


def scan_folder(folder):
    """Scan image files in a folder."""
    files = []
    extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
    for root, _, names in os.walk(folder):
        for name in names:
            if name.lower().endswith(extensions):
                files.append(os.path.join(root, name))
    return files
