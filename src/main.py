import tkinter as tk
from tkinter import filedialog

from scanner import scan_folder
from hashing import calculate_hash
from duplicate import find_duplicates_from_rows


def scan_and_find():
    folder = filedialog.askdirectory()
    if not folder:
        return

    label.config(text="Scanning...")
    root.update()

    rows = []
    files = scan_folder(folder)

    for path in files:
        try:
            file_hash = calculate_hash(path)
            rows.append((path, file_hash))
        except Exception:
            pass

    duplicates = find_duplicates_from_rows(rows)

    text.delete("1.0", tk.END)
    text.insert(tk.END, f"Files: {len(files)}\n")
    text.insert(tk.END, f"Duplicate groups: {len(duplicates)}\n\n")

    for index, group in enumerate(duplicates, 1):
        text.insert(tk.END, f"Group {index}\n")
        for path in group:
            text.insert(tk.END, f"  {path}\n")
        text.insert(tk.END, "\n")

    label.config(text="Completed")


root = tk.Tk()
root.title("QPhotoCleaner v0.1")
root.geometry("700x500")

button = tk.Button(root, text="Select Folder and Scan", command=scan_and_find)
button.pack(pady=10)

label = tk.Label(root, text="Ready")
label.pack()

text = tk.Text(root)
text.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()
