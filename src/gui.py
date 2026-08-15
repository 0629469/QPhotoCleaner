"""
QPhotoCleaner GUI
Version 1.4.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

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

    def add_file(self, row):
        group = row["duplicate"]
        if group not in self.keep_map:
            self.keep_map[group] = row["path"]
        keep = "✓" if self.keep_map[group] == row["path"] else ""
        modified = datetime.datetime.fromtimestamp(row["modified"]).strftime("%Y-%m-%d %H:%M:%S")
        size_mb = row["size"] / 1024 / 1024
        self.rows.append(row)
        self.tree.insert("", "end", iid=str(len(self.rows) - 1), values=(
            keep, row["duplicate"], row["filename"], f"{size_mb:.2f} MB", row["extension"], modified
        ))

    def load_duplicates(self, rows):
        self.clear()
        for row in rows:
            self.add_file(row)

    def refresh_keep_column(self):
        for index, row in enumerate(self.rows):
            values = list(self.tree.item(str(index), "values"))
            if values:
                values[0] = "✓" if self.keep_map.get(row["duplicate"]) == row["path"] else ""
                self.tree.item(str(index), values=values)

    def set_keep(self, row):
        self.keep_map[row["duplicate"]] = row["path"]
        self.refresh_keep_column()

    def on_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item:
            return
        if column == "#1":
            row = self.rows[int(item)]
            self.set_keep(row)
            self.tree.selection_set(item)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        row = self.rows[int(item)]
        self.set_keep(row)
        self.tree.selection_set(item)

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        row = self.rows[int(selection[0])]
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
        messagebox.showinfo("削除候補の確認", f"削除候補 : {len(delete_files)} 件\n\nKeepに指定されていないファイルです。\n現在はまだファイルを移動しません。")

    def move_delete_files(self):
        delete_files = self.get_delete_files()
        if not delete_files:
            messagebox.showinfo("QPhotoCleaner", "ごみ箱へ移動するファイルはありません。")
            return
        if not messagebox.askyesno("ごみ箱へ移動", f"Keep以外の {len(delete_files)} 件をWindowsのごみ箱へ移動します。\n\nKeepに指定したファイルは移動しません。\n\n実行しますか？"):
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
