"""
QPhotoCleaner
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from scanner import scan_folder
from database import create_database


def main():

    root = tk.Tk()
    root.withdraw()

    create_database()

    folder = filedialog.askdirectory(
        title="スキャンするフォルダーを選択してください"
    )

    if not folder:
        return

    files = scan_folder(folder)

    images = sum(1 for f in files if f["media_type"] == "image")
    videos = sum(1 for f in files if f["media_type"] == "video")

    messagebox.showinfo(

        "結果",

        f"画像 {images}枚\n"

        f"動画 {videos}本\n\n"

        f"SQLiteデータベースを作成しました。"

    )


if __name__ == "__main__":
    main()