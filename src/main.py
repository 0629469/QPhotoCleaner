"""
QPhotoCleaner
Main Program
Version 1.0
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

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

    print("=" * 60)
    print("QPhotoCleaner Version 1.0")
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

    print()

    print("SQLite登録中...")

    db = Database()

    db.create()
    db.clear()

    for file in files:
        db.insert(file)

    db.commit()

    print(f"SQLite登録 : {db.count()} 件")

    print()

    print("SHA-256計算中...")

    engine = DuplicateEngine(db)

    engine.calculate_hashes()

    duplicate_file_count = engine.show_duplicates()

    duplicate_group_count = db.get_group_count()

    db.close()

    print()
    print("=" * 60)
    print("完了")
    print("=" * 60)

    messagebox.showinfo(

        "QPhotoCleaner",

        f"""
スキャン完了

画像ファイル
    {image_count} 件

動画ファイル
    {video_count} 件

SQLite登録
    {len(files)} 件

重複グループ
    {duplicate_group_count} グループ

重複ファイル
    {duplicate_file_count} 件
"""

    )

    root.destroy()


if __name__ == "__main__":
    main()