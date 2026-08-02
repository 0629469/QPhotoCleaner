import tkinter as tk
from tkinter import filedialog

from scanner import scan_folder


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        result = scan_folder(folder)
        label.config(text=f"Scanned files: {len(result)}")


root = tk.Tk()
root.title("QPhotoCleaner")
root.geometry("400x200")

button = tk.Button(root, text="Select Folder", command=select_folder)
button.pack(pady=30)

label = tk.Label(root, text="Ready")
label.pack()

root.mainloop()
