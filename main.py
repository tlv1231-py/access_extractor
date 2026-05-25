import tkinter as tk

from ui.app import App

root = tk.Tk()
root.title("Access Extractor")
App(root).pack(fill="both", expand=True)
root.mainloop()
