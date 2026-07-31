"""
QPhotoCleaner
Main Program
GUI Version
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from scanner import scan_folder
from database import Database
from duplicate import DuplicateEngine


def main():

    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(
        title="スキャンするフォルダを選択してください"
    )

    if not folder:
        return

    print("=" * 50)
    print("QPhotoCleaner")
    print("=" * 50)

    print("スキャン中...")

    files = scan_folder(folder)

    images = sum(
        1 for f in files
        if f["media_type"] == "image"
    )

    videos = sum(
        1 for f in files
        if f["media_type"] == "video"
    )

    print("SQLite登録中...")

    db = Database()

    db.create()
    db.clear()

    for file in files:
        db.insert(file)

    db.commit()

    print("SHA-256計算中...")

    engine = DuplicateEngine(db)

    engine.calculate_hashes()

    duplicate_count = engine.show_duplicates()

    count = db.count()

    db.close()

    messagebox.showinfo(
        "QPhotoCleaner",
        f"""スキャン完了

画像 : {images}

動画 : {videos}

SQLite登録 : {count} 件

重複ファイル : {duplicate_count} 件
"""
    )


if __name__ == "__main__":
    main()