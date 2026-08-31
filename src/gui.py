"""
QPhotoCleaner
GUI
Version 2.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from thumbnail import ThumbnailEngine
from imageinfo import ImageInfo
from delete import DeleteEngine


class ResultWindow:

    def __init__(self):
        self.thumbnail = ThumbnailEngine((300, 300))
        self.delete_engine = DeleteEngine()

        self.rows = []
        self.keep_map = {}

        # -----------------------------------------------------
        # Delete progress
        # -----------------------------------------------------

        self.delete_progress_window = None
        self.delete_progress_bar = None
        self.delete_progress_status = None
        self.delete_progress_filename = None
        self.delete_progress_result = None

        self.delete_success_count = 0
        self.delete_failure_count = 0

        self.root = tk.Tk()
        self.root.title("QPhotoCleaner")
        self.root.geometry("1400x800")

        self.create_widgets()

    # =========================================================
    # GUI
    # =========================================================

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

        headings = (
            "Keep",
            "Group",
            "File Name",
            "Size",
            "Type",
            "Modified"
        )

        for column, heading in zip(
            columns,
            headings
        ):
            self.tree.heading(
                column,
                text=heading
            )

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

        # -----------------------------------------------------
        # Thumbnail
        # -----------------------------------------------------

        self.thumbnail_label = tk.Label(
            right,
            width=300,
            height=300,
            relief="solid"
        )

        self.thumbnail_label.pack(
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # File information
        # -----------------------------------------------------

        self.info_filename = tk.Label(
            right,
            anchor="w",
            justify="left"
        )

        self.info_filename.pack(
            fill="x"
        )

        self.info_resolution = tk.Label(
            right,
            anchor="w",
            justify="left"
        )

        self.info_resolution.pack(
            fill="x"
        )

        self.info_taken = tk.Label(
            right,
            anchor="w",
            justify="left"
        )

        self.info_taken.pack(
            fill="x"
        )

        self.info_size = tk.Label(
            right,
            anchor="w",
            justify="left"
        )

        self.info_size.pack(
            fill="x"
        )

        self.info_sha = tk.Label(
            right,
            anchor="w",
            justify="left",
            wraplength=300
        )

        self.info_sha.pack(
            fill="x"
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.review_button = tk.Button(
            right,
            text="削除候補を確認",
            command=self.review_delete_files
        )

        self.review_button.pack(
            fill="x",
            pady=(20, 5)
        )

        self.delete_button = tk.Button(
            right,
            text="Keep以外をごみ箱へ移動",
            command=self.move_delete_files
        )

        self.delete_button.pack(
            fill="x",
            pady=5
        )

        # -----------------------------------------------------
        # Events
        # -----------------------------------------------------

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

        self.tree.bind(
            "<Button-1>",
            self.on_click
        )

        self.tree.bind(
            "<Double-1>",
            self.on_double_click
        )

    # =========================================================
    # Clear
    # =========================================================

    def clear(self):

        self.rows.clear()
        self.keep_map.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.thumbnail_label.config(
            image=""
        )

        self.thumbnail_label.image = None

        self.info_filename.config(text="")
        self.info_resolution.config(text="")
        self.info_taken.config(text="")
        self.info_size.config(text="")
        self.info_sha.config(text="")

    # =========================================================
    # Copy name detection
    # =========================================================

    def is_copy_name(
        self,
        filename
    ):

        name = filename.lower()

        keywords = (
            "コピー",
            "copy",
            "_copy",
            "-copy",
            "_コピー",
            "-コピー",
            "(1)",
            "(2)",
            "(3)",
            "(4)",
            "(5)",
            "(6)",
            "(7)",
            "(8)",
            "(9)"
        )

        return any(
            keyword in name
            for keyword in keywords
        )

    # =========================================================
    # Initial KEEP selection
    # =========================================================

    def select_initial_keep(
        self,
        group_rows
    ):

        if not group_rows:
            return None

        normal_files = []
        copy_files = []

        for row in group_rows:

            if self.is_copy_name(
                row["filename"]
            ):

                copy_files.append(row)

            else:

                normal_files.append(row)

        if normal_files:

            normal_files.sort(
                key=lambda row: (
                    len(row["filename"]),
                    row["filename"].lower()
                )
            )

            return normal_files[0]["path"]

        return copy_files[0]["path"]

    # =========================================================
    # Load duplicate groups
    # =========================================================

    def load_duplicates(
        self,
        rows
    ):

        self.clear()

        self.rows = list(rows)

        groups = {}

        for row in self.rows:

            group = row["duplicate"]

            if group not in groups:

                groups[group] = []

            groups[group].append(row)

        for group, group_rows in groups.items():

            self.keep_map[group] = (
                self.select_initial_keep(
                    group_rows
                )
            )

        for index, row in enumerate(
            self.rows
        ):

            self.insert_row(
                index,
                row
            )

    # =========================================================
    # Insert row
    # =========================================================

    def insert_row(
        self,
        index,
        row
    ):

        import datetime

        group = row["duplicate"]

        keep = ""

        if self.keep_map.get(
            group
        ) == row["path"]:

            keep = "✓"

        modified = (
            datetime.datetime
            .fromtimestamp(
                row["modified"]
            )
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        size_mb = (
            row["size"]
            / 1024
            / 1024
        )

        self.tree.insert(
            "",
            "end",
            iid=f"row_{index}",
            values=(
                keep,
                group,
                row["filename"],
                f"{size_mb:.2f} MB",
                row["extension"],
                modified
            )
        )

    # =========================================================
    # Refresh KEEP column
    # =========================================================

    def refresh_keep_column(self):

        for index, row in enumerate(
            self.rows
        ):

            item_id = f"row_{index}"

            if not self.tree.exists(
                item_id
            ):

                continue

            values = list(
                self.tree.item(
                    item_id,
                    "values"
                )
            )

            if values:

                if self.keep_map.get(
                    row["duplicate"]
                ) == row["path"]:

                    values[0] = "✓"

                else:

                    values[0] = ""

                self.tree.item(
                    item_id,
                    values=values
                )

    # =========================================================
    # Set KEEP
    # =========================================================

    def set_keep(
        self,
        row
    ):

        group = row["duplicate"]

        self.keep_map[group] = row["path"]

        self.refresh_keep_column()

    # =========================================================
    # Mouse click
    # =========================================================

    def on_click(
        self,
        event
    ):

        item = self.tree.identify_row(
            event.y
        )

        column = self.tree.identify_column(
            event.x
        )

        if not item:

            return

        if column != "#1":

            return

        index = self.get_row_index(
            item
        )

        if index is None:

            return

        self.set_keep(
            self.rows[index]
        )

        self.tree.selection_set(
            item
        )

    # =========================================================
    # Double click
    # =========================================================

    def on_double_click(
        self,
        event
    ):

        item = self.tree.identify_row(
            event.y
        )

        if not item:

            return

        index = self.get_row_index(
            item
        )

        if index is None:

            return

        self.set_keep(
            self.rows[index]
        )

        self.tree.selection_set(
            item
        )

    # =========================================================
    # Treeview ID -> row index
    # =========================================================

    def get_row_index(
        self,
        item
    ):

        if not item.startswith(
            "row_"
        ):

            return None

        try:

            index = int(
                item[4:]
            )

        except ValueError:

            return None

        if index < 0:

            return None

        if index >= len(
            self.rows
        ):

            return None

        return index

    # =========================================================
    # Selection
    # =========================================================

    def on_select(
        self,
        event
    ):

        selection = self.tree.selection()

        if not selection:

            return

        index = self.get_row_index(
            selection[0]
        )

        if index is None:

            return

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
            text=(
                "Resolution : "
                + ImageInfo.format_resolution(
                    info["width"],
                    info["height"]
                )
            )
        )

        self.info_taken.config(
            text=f"Taken : {info['taken']}"
        )

        self.info_size.config(
            text=(
                "File Size : "
                + ImageInfo.format_size(
                    info["filesize"]
                )
            )
        )

        self.info_sha.config(
            text=f"SHA256 : {row['sha256']}"
        )

    # =========================================================
    # KEEP files
    # =========================================================

    def get_keep_files(self):

        return [
            row["path"]
            for row in self.rows
            if self.keep_map.get(
                row["duplicate"]
            ) == row["path"]
        ]

    # =========================================================
    # Delete candidates
    # =========================================================

    def get_delete_files(self):

        return [
            row["path"]
            for row in self.rows
            if self.keep_map.get(
                row["duplicate"]
            ) != row["path"]
        ]

    # =========================================================
    # DELETE CANDIDATE REVIEW
    # =========================================================

    def review_delete_files(self):

        delete_files = (
            self.get_delete_files()
        )

        if not delete_files:

            messagebox.showinfo(
                "QPhotoCleaner",
                "削除候補はありません。"
            )

            return

        dialog = tk.Toplevel(
            self.root
        )

        dialog.title(
            "削除候補の確認"
        )

        dialog.geometry(
            "1000x600"
        )

        dialog.transient(
            self.root
        )

        dialog.grab_set()

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = tk.Label(
            dialog,
            text=(
                f"削除候補 : "
                f"{len(delete_files)} 件\n\n"
                "以下のファイルはKeepに指定されていません。"
            ),
            anchor="w",
            justify="left"
        )

        header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # -----------------------------------------------------
        # List
        # -----------------------------------------------------

        frame = tk.Frame(
            dialog
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        listbox = tk.Listbox(
            frame
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=listbox.yview
        )

        listbox.configure(
            yscrollcommand=scrollbar.set
        )

        listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for path in delete_files:

            listbox.insert(
                "end",
                path
            )

        # -----------------------------------------------------
        # Close
        # -----------------------------------------------------

        close_button = tk.Button(
            dialog,
            text="閉じる",
            command=dialog.destroy
        )

        close_button.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
    # =========================================================
    # Move to recycle bin
    # =========================================================

    def move_delete_files(self):

        delete_files = (
            self.get_delete_files()
        )

        if not delete_files:

            messagebox.showinfo(
                "QPhotoCleaner",
                "ごみ箱へ移動するファイルはありません。"
            )

            return

        result = messagebox.askyesno(
            "ごみ箱へ移動",
            (
                f"Keep以外の "
                f"{len(delete_files)} 件を"
                "ごみ箱へ移動します。\n\n"
                "Keepに指定したファイルは移動しません。\n\n"
                "実行しますか？"
            )
        )

        if not result:

            return

        # -----------------------------------------------------
        # Reset progress counters
        # -----------------------------------------------------

        self.delete_success_count = 0
        self.delete_failure_count = 0

        # -----------------------------------------------------
        # Disable buttons while processing
        # -----------------------------------------------------

        self.delete_button.config(
            state="disabled"
        )

        self.review_button.config(
            state="disabled"
        )

        # -----------------------------------------------------
        # Show progress window
        # -----------------------------------------------------

        self.show_delete_progress(
            len(delete_files)
        )

        # -----------------------------------------------------
        # Run delete operation in background thread
        # -----------------------------------------------------

        thread = threading.Thread(
            target=self.delete_files_worker,
            args=(delete_files,),
            daemon=True
        )

        thread.start()

    # =========================================================
    # Delete progress window
    # =========================================================

    def show_delete_progress(
        self,
        total
    ):

        self.delete_progress_window = tk.Toplevel(
            self.root
        )

        self.delete_progress_window.title(
            "ごみ箱へ移動中"
        )

        self.delete_progress_window.geometry(
            "650x250"
        )

        self.delete_progress_window.transient(
            self.root
        )

        self.delete_progress_window.resizable(
            False,
            False
        )

        frame = tk.Frame(
            self.delete_progress_window
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.delete_progress_status = tk.Label(
            frame,
            text=(
                "ごみ箱へ移動しています...\n"
                f"0 / {total} 件"
            ),
            anchor="w",
            justify="left"
        )

        self.delete_progress_status.pack(
            fill="x",
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # Progress bar
        # -----------------------------------------------------

        self.delete_progress_bar = ttk.Progressbar(
            frame,
            orient="horizontal",
            mode="determinate",
            maximum=total
        )

        self.delete_progress_bar.pack(
            fill="x",
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # Current file
        # -----------------------------------------------------

        self.delete_progress_filename = tk.Label(
            frame,
            text="",
            anchor="w",
            justify="left"
        )

        self.delete_progress_filename.pack(
            fill="x"
        )

        # -----------------------------------------------------
        # Result count
        # -----------------------------------------------------

        self.delete_progress_result = tk.Label(
            frame,
            text="成功 : 0 件    失敗 : 0 件",
            anchor="w",
            justify="left"
        )

        self.delete_progress_result.pack(
            fill="x",
            pady=(10, 0)
        )

    # =========================================================
    # Delete worker
    # =========================================================

    def delete_files_worker(
        self,
        delete_files
    ):

        def progress_callback(
            processed,
            total,
            filepath,
            success
        ):

            self.root.after(
                0,
                self.update_delete_progress,
                processed,
                total,
                filepath,
                success
            )

        try:

            result = (
                self.delete_engine
                .move_files_to_trash(
                    delete_files,
                    progress_callback
                )
            )

            self.root.after(
                0,
                self.delete_finished,
                delete_files,
                result
            )

        except Exception as error:

            self.root.after(
                0,
                self.delete_failed,
                str(error)
            )

    # =========================================================
    # Update delete progress
    # =========================================================

    def update_delete_progress(
        self,
        processed,
        total,
        filepath,
        success
    ):

        if (
            self.delete_progress_window
            is None
        ):

            return

        if not self.delete_progress_window.winfo_exists():

            return

        self.delete_progress_bar["value"] = (
            processed
        )

        self.delete_progress_status.config(
            text=(
                "ごみ箱へ移動しています...\n"
                f"{processed} / {total} 件"
            )
        )

        self.delete_progress_filename.config(
            text=(
                "処理済み:\n"
                f"{filepath}"
            )
        )

        if success:

            self.delete_success_count += 1

        else:

            self.delete_failure_count += 1

        self.delete_progress_result.config(
            text=(
                f"成功 : "
                f"{self.delete_success_count} 件    "
                f"失敗 : "
                f"{self.delete_failure_count} 件"
            )
        )

    # =========================================================
    # Delete finished
    # =========================================================

    def delete_finished(
        self,
        delete_files,
        result
    ):

        (
            success_count,
            failure_count,
            failed_files
        ) = result

        if (
            self.delete_progress_window
            is not None
        ):

            if self.delete_progress_window.winfo_exists():

                self.delete_progress_window.destroy()

        self.delete_progress_window = None
        self.delete_progress_bar = None
        self.delete_progress_status = None
        self.delete_progress_filename = None
        self.delete_progress_result = None

        self.delete_success_count = 0
        self.delete_failure_count = 0

        # -----------------------------------------------------
        # Re-enable buttons
        # -----------------------------------------------------

        self.delete_button.config(
            state="normal"
        )

        self.review_button.config(
            state="normal"
        )

        message = (
            "ごみ箱への移動が完了しました。\n\n"
            f"成功 : {success_count} 件\n"
            f"失敗 : {failure_count} 件"
        )

        if failed_files:

            message += (
                "\n\n失敗したファイル:\n"
            )

            message += "\n".join(
                failed_files[:10]
            )

            if len(
                failed_files
            ) > 10:

                message += (
                    f"\n...ほか "
                    f"{len(failed_files) - 10} 件"
                )

        messagebox.showinfo(
            "QPhotoCleaner",
            message
        )

        if success_count > 0:

            self.remove_moved_files(
                delete_files,
                failed_files
            )

    # =========================================================
    # Delete failed
    # =========================================================

    def delete_failed(
        self,
        error
    ):

        if (
            self.delete_progress_window
            is not None
        ):

            if self.delete_progress_window.winfo_exists():

                self.delete_progress_window.destroy()

        self.delete_progress_window = None
        self.delete_progress_bar = None
        self.delete_progress_status = None
        self.delete_progress_filename = None
        self.delete_progress_result = None

        self.delete_success_count = 0
        self.delete_failure_count = 0

        self.delete_button.config(
            state="normal"
        )

        self.review_button.config(
            state="normal"
        )

        messagebox.showerror(
            "QPhotoCleaner",
            (
                "ごみ箱への移動中に"
                "エラーが発生しました。\n\n"
                f"{error}"
            )
        )

    # =========================================================
    # Remove moved files
    # =========================================================

    def remove_moved_files(
        self,
        delete_files,
        failed_files
    ):

        failed_set = set(
            failed_files
        )

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

    # =========================================================
    # Run
    # =========================================================

    def run(self):

        self.root.mainloop()