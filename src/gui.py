"""
QPhotoCleaner
GUI
Version 1.4.4
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
        left.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        right.pack(side="right", fill="y", padx=10, pady=10)

        columns = ("keep", "group", "filename", "size", "type", "modified")
        self.tree = ttk.Treeview(left, columns=columns, show="headings")
        for column, title in zip(columns, ("Keep", "Group", "File Name", "Size", "Type", "Modified")):
            self.tree.heading(column, text=title)
        self.tree.column("keep", width=70, anchor="center")
        self.tree.column("group", width=70, anchor="center")
        self.tree.column("filename", width=300)
        self.tree.column("size", width=90, anchor="e")
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("modified", width=170)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.thumbnail_label = tk.Label(right, width=300, height=300, relief="solid")
        self.thumbnail_label.pack(pady=(0, 10))
        self.info_filename = tk.Label(right, anchor="w", justify="left")
        self.info_filename.pack(fill="x")
        self.info_resolution = tk.Label(right, anchor="w", justify="left")
        self.info_resolution.pack(fill="x")
        self.info_taken = tk.Label(right, anchor="w", justify="left")
        self.info_taken.pack(fill="x")
        self.info_size = tk.Label(right, anchor="w", justify="left")
        self.info_size.pack(fill="x")
        self.info_sha = tk.Label(right, anchor="w", justify="left", wraplength=300)
        self.info_sha.pack(fill="x")

        self.review_button = tk.Button(right, text="Keep以外を確認", command=self.review_delete_files)
        self.review_button.pack(fill="x", pady=(20, 5))
        self.delete_button = tk.Button(right, text="Keep以外をごみ箱へ移動", command=self.move_delete_files)
        self.delete_button.pack(fill="x", pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Double-1>", self.on_double_click)

    def clear(self):
        self.rows.clear()
        self.keep_map.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.thumbnail_label.config(image="")
        self.thumbnail_label.image = None
        for widget in (self.info_filename, self.info_resolution, self.info_taken, self.info_size, self.info_sha):
            widget.config(text="")

    def is_copy_name(self, filename):
        name = filename.lower()
        keywords = (
            "コピー", "copy", "_copy", "-copy", "_コピー", "-コピー",
            "(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)"
        )
        return any(keyword in name for keyword in keywords)

    def select_initial_keep(self, group_rows):
        if not group_rows:
            return None
        normal_files = []
        copy_files = []
        for row in group_rows:
            if self.is_copy_name(row["filename"]):
                copy_files.append(row)
            else:
                normal_files.append(row)
        if normal_files:
            normal_files.sort(key=lambda row: (len(row["filename"]), row["filename"].lower()))
            return normal_files[0]["path"]
        return copy_files[0]["path"]

    def load_duplicates(self, rows):
        self.clear()
        self.rows = list(rows)

        groups = {}
        for row in self.rows:
            group = row["duplicate"]
            groups.setdefault(group, []).append(row)

        for group, group_rows in groups.items():
            self.keep_map[group] = self.select_initial_keep(group_rows)

        for index, row in enumerate(self.rows):
            self.insert_row(index, row)

    def insert_row(self, index, row):
        import datetime
        group = row["duplicate"]
        keep = "✓" if self.keep_map.get(group) == row["path"] else ""
        modified = datetime.datetime.fromtimestamp(row["modified"]).strftime("%Y-%m-%d %H:%M:%S")
        size_mb = row["size"] / 1024 / 1024
        self.tree.insert(
            "", "end", iid=f"row_{index}",
            values=(keep, group, row["filename"], f"{size_mb:.2f} MB", row["extension"], modified)
        )

    def refresh_keep_column(self):
        for index, row in enumerate(self.rows):
            item_id = f"row_{index}"
            if not self.tree.exists(item_id):
                continue
            values = list(self.tree.item(item_id, "values"))
            if values:
                values[0] = "✓" if self.keep_map.get(row["duplicate"]) == row["path"] else ""
                self.tree.item(item_id, values=values)

    def set_keep(self, row):
        self.keep_map[row["duplicate"]] = row["path"]
        self.refresh_keep_column()

    def on_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or column != "#1":
            return
        index = self.get_row_index(item)
        if index is None:
            return
        self.set_keep(self.rows[index])
        self.tree.selection_set(item)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        index = self.get_row_index(item)
        if index is None:
            return
        self.set_keep(self.rows[index])
        self.tree.selection_set(item)

    def get_row_index(self, item):
        if not item.startswith("row_"):
            return None
        try:
            index = int(item[4:])
        except ValueError:
            return None
        if index < 0 or index >= len(self.rows):
            return None
        return index

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        index = self.get_row_index(selection[0])
        if index is None:
            return
        row = self.rows[index]
        photo = self.thumbnail.load(row["path"])
        if photo:
            self.thumbnail_label.configure(image=photo)
            self.thumbnail_label.image = photo
        else:
            self.thumbnail_label.configure(image="")
            self.thumbnail_label.image = None
        info = ImageInfo.get(row["path"])
        self.info_filename.config(text=f"File : {row['filename']}")
        self.info_resolution.config(text="Resolution : " + ImageInfo.format_resolution(info["width"], info["height"]))
        self.info_taken.config(text=f"Taken : {info['taken']}")
        self.info_size.config(text="File Size : " + ImageInfo.format_size(info["filesize"]))
        self.info_sha.config(text=f"SHA256 : {row['sha256']}")

    def get_selected(self):
        return self.tree.selection()

    def get_keep_files(self):
        return [row["path"] for row in self.rows if self.keep_map.get(row["duplicate"]) == row["path"]]

    def get_delete_files(self):
        return [row["path"] for row in self.rows if self.keep_map.get(row["duplicate"]) != row["path"]]

    def review_delete_files(self):
        delete_files = self.get_delete_files()
        if not delete_files:
            messagebox.showinfo("QPhotoCleaner", "削除候補はありません。")
            return
        messagebox.showinfo(
            "削除候補の確認",
            f"削除候補 : {len(delete_files)} 件\n\nKeepに指定されていないファイルです。\n現在はまだファイルを移動しません。"
        )

    def move_delete_files(self):
        delete_files = self.get_delete_files()
        if not delete_files:
            messagebox.showinfo("QPhotoCleaner", "ごみ箱へ移動するファイルはありません。")
            return
        if not messagebox.askyesno(
            "ごみ箱へ移動",
            f"Keep以外の {len(delete_files)} 件をWindowsのごみ箱へ移動します。\n\nKeepに指定したファイルは移動しません。\n\n実行しますか？"
        ):
            return
        success_count, failure_count, failed_files = self.delete_engine.move_files_to_trash(delete_files)
        message = f"ごみ箱への移動が完了しました。\n\n成功 : {success_count} 件\n失敗 : {failure_count} 件"
        if failed_files:
            message += "\n\n失敗したファイル:\n" + "\n".join(failed_files[:10])
            if len(failed_files) > 10:
                message += f"\n...ほか {len(failed_files) - 10} 件"
        messagebox.showinfo("QPhotoCleaner", message)
        if success_count > 0:
            self.remove_moved_files(delete_files, failed_files)

    def remove_moved_files(self, delete_files, failed_files):
        failed_set = set(failed_files)
        moved_paths = [path for path in delete_files if path not in failed_set]
        if not moved_paths:
            return
        self.load_duplicates([row for row in self.rows if row["path"] not in moved_paths])

    def run(self):
        self.root.mainloop()
