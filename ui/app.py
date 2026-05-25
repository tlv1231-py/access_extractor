import pathlib
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext

from extractor.engine.runner import ExtractionJob, run_extraction


class App(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self._build_ui()

    # ------------------------------------------------------------------
    # Layout

    def _build_ui(self) -> None:
        pad = {"padx": 8, "pady": 4}

        tk.Label(self, text="MDB Path").grid(row=0, column=0, sticky="w", **pad)
        self._mdb_var = tk.StringVar()
        tk.Entry(self, textvariable=self._mdb_var, width=60).grid(row=0, column=1, sticky="ew", **pad)
        tk.Button(self, text="Browse…", command=self._browse_mdb).grid(row=0, column=2, **pad)

        tk.Label(self, text="Output Path").grid(row=1, column=0, sticky="w", **pad)
        self._output_var = tk.StringVar()
        tk.Entry(self, textvariable=self._output_var, width=60).grid(row=1, column=1, sticky="ew", **pad)
        tk.Button(self, text="Browse…", command=self._browse_output).grid(row=1, column=2, **pad)

        self._run_btn = tk.Button(self, text="Run", command=self._run, width=12)
        self._run_btn.grid(row=2, column=0, columnspan=3, pady=8)

        self._status_var = tk.StringVar(value="idle")
        tk.Label(self, textvariable=self._status_var, anchor="w").grid(
            row=3, column=0, columnspan=3, sticky="w", **pad
        )

        self._log = scrolledtext.ScrolledText(
            self, height=16, state="disabled", wrap="word"
        )
        self._log.grid(row=4, column=0, columnspan=3, sticky="nsew", **pad)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    # ------------------------------------------------------------------
    # Browse

    def _browse_mdb(self) -> None:
        path = filedialog.askopenfilename(
            title="Select Access database",
            filetypes=[("Access databases", "*.mdb *.accdb"), ("All files", "*.*")],
        )
        if path:
            self._mdb_var.set(path)

    def _browse_output(self) -> None:
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self._output_var.set(directory)

    # ------------------------------------------------------------------
    # Run

    def _run(self) -> None:
        mdb = self._mdb_var.get().strip()
        output_dir = self._output_var.get().strip()

        if not mdb or not output_dir:
            self._append_log("Please set both MDB Path and Output Path.")
            return

        output_path = str(pathlib.Path(output_dir) / (pathlib.Path(mdb).stem + ".json"))
        job = ExtractionJob(mdb_path=mdb, output_path=output_path)

        self._run_btn.config(state="disabled")
        self._status_var.set("running")
        self._clear_log()
        self._append_log(f"Input:  {mdb}")
        self._append_log(f"Output: {output_path}")
        self._append_log("Running…")

        threading.Thread(target=self._worker, args=(job,), daemon=True).start()

    def _worker(self, job: ExtractionJob) -> None:
        try:
            summary = run_extraction(job)
            self.after(0, self._on_success, summary)
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _on_success(self, summary: dict) -> None:
        self._status_var.set("done")
        self._run_btn.config(state="normal")
        self._append_log("Extraction complete.\n")
        for key, val in summary.items():
            self._append_log(f"  {key}: {val}")

    def _on_error(self, message: str) -> None:
        self._status_var.set("error")
        self._run_btn.config(state="normal")
        self._append_log(f"\nError: {message}")

    # ------------------------------------------------------------------
    # Log helpers

    def _clear_log(self) -> None:
        self._log.config(state="normal")
        self._log.delete("1.0", tk.END)
        self._log.config(state="disabled")

    def _append_log(self, message: str) -> None:
        self._log.config(state="normal")
        self._log.insert(tk.END, message + "\n")
        self._log.see(tk.END)
        self._log.config(state="disabled")


def main() -> None:
    root = tk.Tk()
    root.title("Access Extractor")
    App(root).pack(fill="both", expand=True)
    root.mainloop()
