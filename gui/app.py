import threading
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core import converter
from core import downloader

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("pybeta")
        self.geometry("560x360")

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=12, pady=12)
        tabview.add("Download")
        tabview.add("Convert")

        self._build_download_tab(tabview.tab("Download"))
        self._build_convert_tab(tabview.tab("Convert"))

    # ---------- Download tab ----------
    def _build_download_tab(self, tab):
        self.url_var = ctk.StringVar()
        ctk.CTkEntry(tab, textvariable=self.url_var, width=400,
                     placeholder_text="YouTube URL").pack(pady=10)

        self.audio_only_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(tab, text="Audio only (mp3)",
                         variable=self.audio_only_var).pack(pady=5)

        self.dl_progress = ctk.CTkProgressBar(tab, width=400)
        self.dl_progress.set(0)
        self.dl_progress.pack(pady=15)

        self.dl_status = ctk.CTkLabel(tab, text="")
        self.dl_status.pack()

        ctk.CTkButton(tab, text="Download", command=self._start_download).pack(pady=10)

    def _start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("pybeta", "Enter a URL first.")
            return
        threading.Thread(target=self._run_download, args=(url,), daemon=True).start()

    def _run_download(self, url):
        def on_progress(d):
            if d.get("status") == "downloading":
                pct_str = d.get("_percent_str", "0%").strip().replace("%", "")
                try:
                    pct = float(pct_str) / 100
                except ValueError:
                    pct = 0
                self.after(0, self.dl_progress.set, pct)
                self.after(0, self.dl_status.configure, {"text": f"Downloading... {pct_str}%"})
            elif d.get("status") == "finished":
                self.after(0, self.dl_status.configure, {"text": "Processing..."})

        try:
            path = downloader.download(url, str(Path.home() / "Downloads"),
                                        audio_only=self.audio_only_var.get(),
                                        progress_callback=on_progress)
            self.after(0, self.dl_progress.set, 1)
            self.after(0, self.dl_status.configure, {"text": f"Done: {Path(path).name}"})
        except Exception as e:
            self.after(0, self.dl_status.configure, {"text": f"Error: {e}"})

    # ---------- Convert tab ----------
    def _build_convert_tab(self, tab):
        self.in_file_var = ctk.StringVar()
        ctk.CTkEntry(tab, textvariable=self.in_file_var, width=350).pack(pady=10)
        ctk.CTkButton(tab, text="Browse", command=self._pick_file).pack()

        self.target_var = ctk.StringVar(value="mp3")
        ctk.CTkOptionMenu(tab, variable=self.target_var,
                           values=["mp4", "mp3", "gif", "png", "jpg", "webp"]).pack(pady=10)

        self.conv_progress = ctk.CTkProgressBar(tab, width=400)
        self.conv_progress.set(0)
        self.conv_progress.pack(pady=15)

        self.conv_status = ctk.CTkLabel(tab, text="")
        self.conv_status.pack()

        ctk.CTkButton(tab, text="Convert", command=self._start_convert).pack(pady=10)

    def _pick_file(self):
        f = filedialog.askopenfilename()
        if f:
            self.in_file_var.set(f)

    def _start_convert(self):
        in_path = self.in_file_var.get()
        if not in_path:
            messagebox.showwarning("pybeta", "Pick a file first.")
            return
        threading.Thread(target=self._run_convert,
                          args=(in_path, self.target_var.get()), daemon=True).start()

    def _run_convert(self, input_path, target_format):
        def on_progress(status_text, percent):
            self.after(0, self.conv_progress.set, percent)
            self.after(0, self.conv_status.configure,
                       {"text": f"{status_text} {percent:.0%}"})

        out_path = str(Path(input_path).with_suffix(f".{target_format}"))
        try:
            converter.convert(input_path, out_path, progress_callback=on_progress)
            self.after(0, self.conv_progress.set, 1)
            self.after(0, self.conv_status.configure, {"text": f"Done: {Path(out_path).name}"})
        except Exception as e:
            self.after(0, self.conv_status.configure, {"text": f"Error: {e}"})

def run():
    app = App()
    app.mainloop()