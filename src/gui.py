"""
QPhotoCleaner
GUI
Version 1.2
"""

import tkinter as tk
from tkinter import ttk

from thumbnail import ThumbnailEngine
from imageinfo import ImageInfo


class ResultWindow:

    def __init__(self):

        self.thumbnail = ThumbnailEngine((300, 300))

        self.rows = []

        self.root = tk.Tk()

        self.root.title("QPhotoCleaner")

        self.root.geometry("1300x750")

        self.create_widgets()

    def create_widgets(self):

        #
        # 左右フレーム
        #

        left = tk.Frame(self.root)

        right = tk.Frame(self.root)

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )

        right.pack(
            side="right",
            fill="y",
            padx=10,
            pady=10
        )

        #
        # TreeView
        #

        columns = (
            "group",
            "filename",
            "size",
            "type",
            "modified"
        )

        self.tree = ttk.Treeview(
            left,
            columns=columns,
            show="headings"
        )

        self.tree.heading("group", text="Group")
        self.tree.heading("filename", text="File Name")
        self.tree.heading("size", text="Size")
        self.tree.heading("type", text="Type")
        self.tree.heading("modified", text="Modified")

        self.tree.column(
            "group",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "filename",
            width=280
        )

        self.tree.column(
            "size",
            width=90,
            anchor="e"
        )

        self.tree.column(
            "type",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "modified",
            width=170
        )

        scrollbar = ttk.Scrollbar(
            left,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        #
        # サムネイル
        #

        self.thumbnail_label = tk.Label(
            right,
            width=300,
            height=300,
            relief="solid"
        )

        self.thumbnail_label.pack(
            pady=(0, 10)
        )

        #
        # 情報表示
        #

        self.info_filename = tk.Label(
            right,
            anchor="w",
            justify="left"
        )
        self.info_filename.pack(fill="x")

        self.info_resolution = tk.Label(
            right,
            anchor="w",
            justify="left"
        )
        self.info_resolution.pack(fill="x")

        self.info_taken = tk.Label(
            right,
            anchor="w",
            justify="left"
        )
        self.info_taken.pack(fill="x")

        self.info_size = tk.Label(
            right,
            anchor="w",
            justify="left"
        )
        self.info_size.pack(fill="x")

        self.info_sha = tk.Label(
            right,
            anchor="w",
            justify="left",
            wraplength=300
        )
        self.info_sha.pack(fill="x")

        #
        # イベント
        #

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )
    def clear(self):
        """
        一覧をクリア
        """

        self.rows.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.thumbnail_label.config(image="")
        self.thumbnail_label.image = None

        self.info_filename.config(text="")
        self.info_resolution.config(text="")
        self.info_taken.config(text="")
        self.info_size.config(text="")
        self.info_sha.config(text="")

    def add_file(self, row):
        """
        TreeViewへ1件追加
        """

        import datetime

        modified = datetime.datetime.fromtimestamp(
            row["modified"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        size_mb = row["size"] / 1024 / 1024

        self.rows.append(row)

        self.tree.insert(
            "",
            "end",
            iid=str(len(self.rows) - 1),
            values=(
                row["duplicate"],
                row["filename"],
                f"{size_mb:.2f} MB",
                row["extension"],
                modified
            )
        )

    def load_duplicates(self, rows):
        """
        重複一覧を表示
        """

        self.clear()

        for row in rows:
            self.add_file(row)

    def on_select(self, event):
        """
        TreeView選択時
        """

        selection = self.tree.selection()

        if not selection:
            return

        index = int(selection[0])

        row = self.rows[index]

        photo = self.thumbnail.load(row["path"])

        if photo:

            self.thumbnail_label.configure(image=photo)
            self.thumbnail_label.image = photo

        else:

            self.thumbnail_label.configure(image="")
            self.thumbnail_label.image = None

        info = ImageInfo.get(row["path"])

        self.info_filename.config(
            text=f"File : {row['filename']}"
        )

        self.info_resolution.config(
            text="Resolution : " +
            ImageInfo.format_resolution(
                info["width"],
                info["height"]
            )
        )

        self.info_taken.config(
            text=f"Taken : {info['taken']}"
        )

        self.info_size.config(
            text="File Size : " +
            ImageInfo.format_size(
                info["filesize"]
            )
        )

        self.info_sha.config(
            text=f"SHA256 : {row['sha256']}"
        )

    def get_selected(self):

        return self.tree.selection()

    def run(self):

        self.root.mainloop()