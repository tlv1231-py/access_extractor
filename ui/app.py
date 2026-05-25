import pathlib
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from extractor.engine.runner import ExtractionJob, run_extraction
from publisher.profiles import save_profile, load_profile, delete_profile, list_profiles


class App(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self._build_ui()
        self._refresh_profiles()

    def _build_ui(self) -> None:
        pad = {"padx": 8, "pady": 4}

        # MDB Path
        tk.Label(self, text="MDB Path").grid(row=0, column=0, sticky="w", **pad)
        self._mdb_var = tk.StringVar()
        tk.Entry(self, textvariable=self._mdb_var, width=55).grid(row=0, column=1, sticky="ew", **pad)
        tk.Button(self, text="Browse…", command=self._browse_mdb).grid(row=0, column=2, **pad)

        # Output Path
        tk.Label(self, text="Output Path").grid(row=1, column=0, sticky="w", **pad)
        self._output_var = tk.StringVar()
        tk.Entry(self, textvariable=self._output_var, width=55).grid(row=1, column=1, sticky="ew", **pad)
        tk.Button(self, text="Browse…", command=self._browse_output).grid(row=1, column=2, **pad)

        # Separator
        tk.Frame(self, height=1, bg="gray").grid(row=2, column=0, columnspan=3, sticky="ew", pady=4)

        # Profile selector
        tk.Label(self, text="Profile").grid(row=3, column=0, sticky="w", **pad)
        self._profile_var = tk.StringVar()
        self._profile_menu = tk.OptionMenu(self, self._profile_var, "")
        self._profile_menu.config(width=30)
        self._profile_menu.grid(row=3, column=1, sticky="w", **pad)
        tk.Button(self, text="Load", command=self._load_profile).grid(row=3, column=2, **pad)

        # GitHub Repo
        tk.Label(self, text="GitHub Repo").grid(row=4, column=0, sticky="w", **pad)
        self._repo_var = tk.StringVar()
        tk.Entry(self, textvariable=self._repo_var, width=55).grid(row=4, column=1, sticky="ew", **pad)

        # GitHub Token
        tk.Label(self, text="GitHub Token").grid(row=5, column=0, sticky="w", **pad)
        self._token_var = tk.StringVar()
        tk.Entry(self, textvariable=self._token_var, width=55, show="*").grid(row=5, column=1, sticky="ew", **pad)

        # Profile name + save/delete
        tk.Label(self, text="Profile Name").grid(row=6, column=0, sticky="w", **pad)
        self._profile_name_var = tk.StringVar()
        tk.Entry(self, textvariable=self._profile_name_var, width=30).grid(row=6, column=1, sticky="w", **pad)
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=2, **pad)
        tk.Button(btn_frame, text="Save", command=self._save_profile).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Delete", command=self._delete_profile).pack(side="left", padx=2)

        # Separator
        tk.Frame(self, height=1, bg="gray").grid(row=7, column=0, columnspan=3, sticky="ew", pady=4)

        # Push toggle
        self._publish_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Push to GitHub after extraction", variable=self._publish_var).grid(
            row=8, column=0, columnspan=3, sticky="w", **pad
        )

        # Run button
        self._run_btn = tk.Button(self, text="Run", command=self._run, width=12)
        self._run_btn.grid(row=9, column=0, columnspan=3, pady=8)

        # Status
        self._status_var = tk.StringVar(value="idle")
        tk.Label(self, textvariable=self._status_var, anchor="w").grid(
            row=10, column=0, columnspan=3, sticky="w", **pad
        )

        # Log
        self._log = scrolledtext.ScrolledText(self, height=16, state="disabled", wrap="word")
        self._log.grid(row=11, column=0, columnspan=3, sticky="nsew", **pad)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(11, weight=1)

    # ------------------------------------------------------------------
    # Profile management

    def _refresh_profiles(self) -> None:
        profiles = list_profiles()
        menu = self._profile_menu["menu"]
        menu.delete(0, "end")
        if profiles:
            for p in profiles:
                menu.add_command(label=p, command=lambda v=p: self._profile_var.set(v))
            self._profile_var.set(profiles[0])
        else:
            self._profile_var.set("")

    def _load_profile(self) -> None:
        name = self._profile_var.get().strip()
        if not name:
            return
        data = load_profile(name)
        if data:
            self._repo_var.set(data.get("repo", ""))
            self._token_var.set(data.get("token", ""))
            self._append_log(f"Loaded profile: {name}")
        else:
            messagebox.showerror("Profile", f"Profile {name!r} not found.")

    def _save_profile(self) -> None:
        name = self._profile_name_var.get().strip()
        repo = self._repo_var.get().strip()
        token = self._token_var.get().strip()
        if not name or not repo or not token:
            messagebox.showerror("Profile", "Profile name, repo, and token are all required.")
            return
        save_profile(name, repo, token)
        self._append_log(f"Saved profile: {name}")
        self._refresh_profiles()
        self._profile_var.set(name)

    def _delete_profile(self) -> None:
        name = self._profile_var.get().strip()
        if not name:
            return
        if messagebox.askyesno("Delete Profile", f"Delete profile {name!r}?"):
            delete_profile(name)
            self._append_log(f"Deleted profile: {name}")
            self._refresh_profiles()

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

        if self._publish_var.get():
            if not self._token_var.get().strip():
                self._append_log("GitHub Token is required when Push to GitHub is enabled.")
                return
            if not self._repo_var.get().strip():
                self._append_log("GitHub Repo is required when Push to GitHub is enabled.")
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
            if self._publish_var.get():
                self.after(0, self._append_log, "Pushing to GitHub…")
                output_dir = pathlib.Path(job.output_path).parent
                publish_results = self._publish(output_dir)
                self.after(0, self._on_publish, publish_results)
                from publisher.github_publisher import GitHubPublisher
                GitHubPublisher(
                    repo=self._repo_var.get().strip(),
                    token=self._token_var.get().strip(),
                ).cleanup(output_dir)
                self.after(0, self._append_log, "Local files cleaned up.")
            self.after(0, self._on_success, summary)
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _publish(self, output_dir: pathlib.Path) -> dict:
        from publisher.github_publisher import GitHubPublisher
        publisher = GitHubPublisher(
            repo=self._repo_var.get().strip(),
            token=self._token_var.get().strip(),
        )
        return publisher.publish(output_dir)

    def _on_publish(self, results: dict) -> None:
        self._append_log("\nGitHub Push Results:")
        for filename, url in results.items():
            self._append_log(f"  {filename}: {url}")

    def _on_success(self, summary: dict) -> None:
        self._status_var.set("done")
        self._run_btn.config(state="normal")
        self._append_log("\nExtraction complete.")
        for key, val in summary.items():
            self._append_log(f"  {key}: {val}")

    def _on_error(self, message: str) -> None:
        self._status_var.set("error")
        self._run_btn.config(state="normal")
        self._append_log(f"\nError: {message}")

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
