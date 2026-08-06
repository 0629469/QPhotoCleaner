"""
QPhotoCleaner
GUI
"""

import tkinter as tk
from tkinter import ttk


class ResultWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("QPhotoCleaner")

        self.root.geometry("1200x700")

        self.root.minsize(900, 500)

        self.create_widgets()

    def create_widgets(self):

        #
        # ===== タイトル =====
        #

        title = tk.Label(

            self.root,

            text="QPhotoCleaner",

            font=("Yu Gothic UI", 18, "bold")

        )

        title.pack(pady=10)

        #
        # ===== TreeView =====
        #

        columns = (

            "group",
            "filename",
            "size",
            "type",
            "modified",
            "path"

        )

        self.tree = ttk.Treeview(

            self.root,

            columns=columns,

            show="headings"

        )

        #
        # 見出し
        #

        self.tree.heading(
            "group",
            text="Group"
        )

        self.tree.heading(
            "filename",
            text="File Name"
        )

        self.tree.heading(
            "size",
            text="Size"
        )

        self.tree.heading(
            "type",
            text="Type"
        )

        self.tree.heading(
            "modified",
            text="Modified"
        )

        self.tree.heading(
            "path",
            text="Path"
        )

        #
        # 列幅
        #

        self.tree.column(
            "group",
            width=70,
            anchor="center"
        )

        self.tree.column(
            "filename",
            width=250
        )

        self.tree.column(
            "size",
            width=100,
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

        self.tree.column(
            "path",
            width=500
        )

        #
        # スクロールバー
        #

        scrollbar_y = ttk.Scrollbar(

            self.root,

            orient="vertical",

            command=self.tree.yview

        )

        scrollbar_x = ttk.Scrollbar(

            self.root,

            orient="horizontal",

            command=self.tree.xview

        )

        self.tree.configure(

            yscrollcommand=scrollbar_y.set,

            xscrollcommand=scrollbar_x.set

        )

        self.tree.pack(

            side="left",

            fill="both",

            expand=True,

            padx=(10, 0),

            pady=(0, 10)

        )

        scrollbar_y.pack(

            side="right",

            fill="y",

            pady=(0, 10)

        )

        scrollbar_x.pack(

            side="bottom",

            fill="x",

            padx=(10, 20)

        )
    def clear(self):
        """
        一覧をクリア
        """

        for item in self.tree.get_children():
            self.tree.delete(item)

    def add_file(self, row):
        """
        TreeViewへ1件追加
        """

        import datetime

        modified = datetime.datetime.fromtimestamp(
            row["modified"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        size_mb = row["size"] / 1024 / 1024

        self.tree.insert(

            "",

            "end",

            values=(

                row["duplicate"],

                row["filename"],

                f"{size_mb:.2f} MB",

                row["extension"],

                modified,

                row["path"]

            )

        )

    def load_duplicates(self, rows):
        """
        重複一覧を表示
        """

        self.clear()

        for row in rows:
            self.add_file(row)

    def get_selected(self):
        """
        選択された行を返す
        """

        return self.tree.selection()

    def run(self):

        self.root.mainloop()