"""
QPhotoCleaner
Main Program
GUI Version
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from scanner import scan_folder
from database import Database


def main():

    root = tk.Tk()
    root.withdraw()

    folder = filedialog.askdirectory(
        title="スキャンするフォルダーを選択してください"
    )

    if not folder:
        return

    db = Database()

    db.create()

    db.clear()

    files = scan_folder(folder)

    for file in files:
        db.insert(file)

    db.commit()

    # calculate_hashes(db)

    count = db.count()

    db.close()

    images = sum(1 for f in files if f["media_type"] == "image")
    videos = sum(1 for f in files if f["media_type"] == "video")

    messagebox.showinfo(

        "QPhotoCleaner",

        f"""スキャン完了

画像 : {images}

動画 : {videos}

SQLite登録 : {count} 件"""

    )


if __name__ == "__main__":
    main()