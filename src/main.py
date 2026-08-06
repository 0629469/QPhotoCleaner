"""
QPhotoCleaner
Main Program
GUI Version
"""

import tkinter as tk
from tkinter import filedialog

from scanner import scan_folder
from database import Database
from duplicate import DuplicateEngine
from gui import ResultWindow


def main():

    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(
        title="スキャンするフォルダを選択してください"
    )

    if not folder:
        return

    print("=" * 60)
    print("QPhotoCleaner")
    print("=" * 60)

    print("スキャン中...")

    files = scan_folder(folder)

    image_count = sum(
        1 for f in files
        if f["media_type"] == "image"
    )

    video_count = sum(
        1 for f in files
        if f["media_type"] == "video"
    )

    print(f"画像 : {image_count}")
    print(f"動画 : {video_count}")

    db = Database()

    db.create()
    db.clear()

    print("SQLite登録中...")

    for file in files:
        db.insert(file)

    db.commit()

    print(f"SQLite登録 : {db.count()} 件")

    print("SHA-256計算中...")

    engine = DuplicateEngine(db)

    engine.calculate_hashes()

    duplicate_count = engine.show_duplicates()

    group_count = db.get_group_count()

    print(f"重複グループ : {group_count}")
    print(f"重複ファイル : {duplicate_count}")

    rows = db.get_duplicate_groups()

    db.close()

    root.destroy()

    #
    # GUI表示
    #

    window = ResultWindow()

    window.load_duplicates(rows)

    window.run()


if __name__ == "__main__":
    main()