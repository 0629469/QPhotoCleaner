"""
QPhotoCleaner
GUI
Version 1.3.3
"""

import tkinter as tk
from tkinter import ttk, messagebox

from thumbnail import ThumbnailEngine
from imageinfo import ImageInfo
from delete import DeleteEngine


class ResultWindow:

    def __init__(self):

        self.thumbnail = ThumbnailEngine((300, 300))

        self.delete_engine = DeleteEngine()

        self.rows = []
        self.keep_map = {}

        self.root = tk.Tk()

        self.root.title("QPhotoCleaner")

        self.root.geometry("1400x800")

        self.create_widgets()

    def create_widgets(self):

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

        columns = (
            "keep",
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

        self.tree.heading("keep", text="Keep")
        self.tree.heading("group", text="Group")
        self.tree.heading("filename", text="File Name")
        self.tree.heading("size", text="Size")
        self.tree.heading("type", text="Type")
        self.tree.heading("modified", text="Modified")

        self.tree.column(
            "keep",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "group",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "filename",
            width=300
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

        self.thumbnail_label = tk.Label(
            right,
            width=300,
            height=300,
            relief="solid"
        )

        self.thumbnail_label.pack(
            pady=(0, 10)
        )

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
        # 削除候補確認
        #

        self.review_button = tk.Button(
            right,
            text="Keep以外を確認",
            command=self.review_delete_files
        )

        self.review_button.pack(
            fill="x",
            pady=(20, 5)
        )

        #
        # ごみ箱移動
        #

        self.delete_button = tk.Button(
            right,
            text="Keep以外をごみ箱へ移動",
            command=self.move_delete_files
        )

        self.delete_button.pack(
            fill="x",
            pady=5
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

        self.tree.bind(
            "<Double-1>",
            self.on_double_click
        )

    def clear(self):

        self.rows.clear()
        self.keep_map.clear()

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

        import datetime

        group = row["duplicate"]

        if group not in self.keep_map:
            self.keep_map[group] = row["path"]

        keep = ""

        if self.keep_map[group] == row["path"]:
            keep = "✓"

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
                keep,
                row["duplicate"],
                row["filename"],
                f"{size_mb:.2f} MB",
                row["extension"],
                modified
            )
        )

    def load_duplicates(self, rows):

        self.clear()

        for row in rows:
            self.add_file(row)

    def refresh_keep_column(self):

        for index, row in enumerate(self.rows):

            keep = ""

            if self.keep_map.get(
                row["duplicate"]
            ) == row["path"]:

                keep = "✓"

            values = list(
                self.tree.item(
                    str(index),
                    "values"
                )
            )

            values[0] = keep

            self.tree.item(
                str(index),
                values=values
            )

    def on_double_click(self, event):

        item = self.tree.identify_row(event.y)

        column = self.tree.identify_column(event.x)

        if not item:
            return

        if column != "#1":
            return

        row = self.rows[int(item)]

        self.keep_map[row["duplicate"]] = row["path"]

        self.refresh_keep_column()

    def on_select(self, event):

        selection = self.tree.selection()

        if not selection:
            return

        index = int(selection[0])

        row = self.rows[index]

        photo = self.thumbnail.load(
            row["path"]
        )

        if photo:

            self.thumbnail_label.configure(
                image=photo
            )

            self.thumbnail_label.image = photo

        else:

            self.thumbnail_label.configure(
                image=""
            )

            self.thumbnail_label.image = None

        info = ImageInfo.get(
            row["path"]
        )

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

    def get_keep_files(self):

        keep_files = []

        for row in self.rows:

            if self.keep_map.get(
                row["duplicate"]
            ) == row["path"]:

                keep_files.append(
                    row["path"]
                )

        return keep_files

    def get_delete_files(self):

        delete_files = []

        for row in self.rows:

            if self.keep_map.get(
                row["duplicate"]
            ) != row["path"]:

                delete_files.append(
                    row["path"]
                )

        return delete_files

    def review_delete_files(self):

        delete_files = self.get_delete_files()

        if not delete_files:

            messagebox.showinfo(
                "QPhotoCleaner",
                "削除候補はありません。"
            )

            return

        message = (
            f"削除候補 : {len(delete_files)} 件\n\n"
            "Keepに指定されていないファイルです。\n"
            "現在はまだファイルを移動しません。"
        )

        messagebox.showinfo(
            "削除候補の確認",
            message
        )

    def move_delete_files(self):

        delete_files = self.get_delete_files()

        if not delete_files:

            messagebox.showinfo(
                "QPhotoCleaner",
                "ごみ箱へ移動するファイルはありません。"
            )

            return

        result = messagebox.askyesno(
            "ごみ箱へ移動",
            (
                f"Keep以外の {len(delete_files)} 件を"
                "Windowsのごみ箱へ移動します。\n\n"
                "Keepに指定したファイルは移動しません。\n\n"
                "実行しますか？"
            )
        )

        if not result:
            return

        success_count, failure_count, failed_files = (
            self.delete_engine.move_files_to_trash(
                delete_files
            )
        )

        message = (
            f"ごみ箱への移動が完了しました。\n\n"
            f"成功 : {success_count} 件\n"
            f"失敗 : {failure_count} 件"
        )

        if failed_files:

            message += "\n\n失敗したファイル:\n"

            for filepath in failed_files[:10]:

                message += (
                    f"{filepath}\n"
                )

            if len(failed_files) > 10:

                message += (
                    f"...ほか {len(failed_files) - 10} 件"
                )

        messagebox.showinfo(
            "QPhotoCleaner",
            message
        )

        #
        # ごみ箱へ移動したファイルを一覧から除去
        #

        if success_count > 0:

            self.remove_moved_files(
                delete_files,
                failed_files
            )

    def remove_moved_files(
        self,
        delete_files,
        failed_files
    ):

        failed_set = set(failed_files)

        moved_paths = [
            path
            for path in delete_files
            if path not in failed_set
        ]

        if not moved_paths:
            return

        remaining_rows = [
            row
            for row in self.rows
            if row["path"] not in moved_paths
        ]

        self.load_duplicates(
            remaining_rows
        )

    def run(self):

        self.root.mainloop()