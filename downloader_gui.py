"""
ADHI Downloader GUI — clickable window version
Run:  python downloader_gui.py
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import yt_dlp
except ImportError:
    raise SystemExit("[!] Run: pip install yt-dlp")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(APP_DIR, "history.json")
import json

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

class Logger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        root.title("ADHI Downloader — GUI")
        root.geometry("640x560")
        root.configure(bg="#14101a")
        root.resizable(False, False)

        self.folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.format_var = tk.StringVar(value="video")
        self.quality_var = tk.StringVar(value="best")
        self.subs_var = tk.BooleanVar(value=False)

        self._build()

    def _build(self):
        f = ttk.Frame(self.root, padding=20)
        f.pack(fill="both", expand=True)

        tk.Label(f, text="ADHI Downloader", font=("Segoe UI", 22, "bold"),
                 fg="#ff9ec7", bg="#14101a").pack()

        tk.Label(f, text="Paste any video link (YouTube, Instagram, TikTok, 1000+ sites)",
                 font=("Segoe UI", 10), fg="#c9b8c4", bg="#14101a").pack(pady=(2, 14))

        self.link = tk.Entry(f, font=("Segoe UI", 12), bg="#241a30", fg="#fff",
                             insertbackground="#fff", relief="flat", width=60)
        self.link.pack(pady=(0, 12), ipady=8)

        opts = tk.Frame(f, bg="#14101a")
        opts.pack(pady=(0, 12))

        tk.Radiobutton(opts, text="Video (MP4)", variable=self.format_var, value="video",
                       bg="#14101a", fg="#fff", selectcolor="#241a30",
                       activebackground="#14101a", activeforeground="#fff",
                       font=("Segoe UI", 11)).grid(row=0, column=0, padx=8)
        tk.Radiobutton(opts, text="Audio (MP3)", variable=self.format_var, value="audio",
                       bg="#14101a", fg="#fff", selectcolor="#241a30",
                       activebackground="#14101a", activeforeground="#fff",
                       font=("Segoe UI", 11)).grid(row=0, column=1, padx=8)
        tk.Checkbutton(opts, text="Subtitles (.srt)", variable=self.subs_var,
                       bg="#14101a", fg="#fff", selectcolor="#241a30",
                       activebackground="#14101a", activeforeground="#fff",
                       font=("Segoe UI", 11)).grid(row=0, column=2, padx=8)

        tk.Label(opts, text="Quality:", bg="#14101a", fg="#c9b8c4",
                 font=("Segoe UI", 11)).grid(row=1, column=0, columnspan=2, pady=(10, 2), sticky="w", padx=8)
        qbox = ttk.Combobox(opts, textvariable=self.quality_var, state="readonly", width=20,
                            values=["best", "2160", "1440", "1080", "720", "480"])
        qbox.grid(row=1, column=2, pady=(10, 2), sticky="w", padx=8)

        btns = tk.Frame(f, bg="#14101a")
        btns.pack(pady=(6, 12))
        self.go_btn = tk.Button(btns, text="⬇  DOWNLOAD", command=self.start,
                                bg="#ff7fb0", fg="#1a0f1e", font=("Segoe UI", 13, "bold"),
                                relief="flat", padx=40, pady=10, cursor="hand2", activebackground="#ff9ec7")
        self.go_btn.grid(row=0, column=0, padx=8)
        tk.Button(btns, text="📁 Folder", command=self.pick_folder,
                  bg="#241a30", fg="#fff", font=("Segoe UI", 11),
                  relief="flat", padx=20, pady=10, cursor="hand2").grid(row=0, column=1, padx=8)

        self.folder_lbl = tk.Label(f, text="Saving to: " + self.folder, bg="#14101a",
                                   fg="#8fd3ff", font=("Segoe UI", 9))
        self.folder_lbl.pack(pady=(0, 8))

        self.bar = ttk.Progressbar(f, length=560, mode="determinate")
        self.bar.pack(pady=(0, 8))

        self.status = tk.Label(f, text="ready...", bg="#14101a", fg="#c9b8c4",
                               font=("Segoe UI", 10), wraplength=560, justify="left")
        self.status.pack()

    def pick_folder(self):
        d = filedialog.askdirectory(initialdir=self.folder)
        if d:
            self.folder = d
            self.folder_lbl.config(text="Saving to: " + d)

    def start(self):
        url = self.link.get().strip()
        if not url:
            messagebox.showwarning("Oops", "Paste a link first!")
            return
        self.go_btn.config(state="disabled", text="Downloading...")
        threading.Thread(target=self.work, args=(url,), daemon=True).start()

    def work(self, url):
        fmt = self.format_var.get()
        q = self.quality_var.get()
        qmap = {"best": "best", "2160": "2160", "1440": "1440", "1080": "1080", "720": "720", "480": "480"}
        quality = qmap.get(q, "best")
        fmt_sel = "bestvideo[height<=?" + quality + "]+bestaudio/best[height<=?" + quality + "]/best" if quality != "best" else "bestvideo+bestaudio/best"

        def hook(d):
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
                pct = d.get("downloaded_bytes", 0) / total * 100
                self.root.after(0, lambda: (self.bar.config(value=pct),
                                            self.status.config(text=f"downloading... {pct:.1f}%  {(d.get('speed') or 0)/1e6:.1f} MB/s")))

        opts = {
            "outtmpl": os.path.join(self.folder, "%(title)s.%(ext)s"),
            "quiet": True, "no_warnings": True, "logger": Logger(),
            "progress_hooks": [hook], "noplaylist": True,
        }
        if fmt == "audio":
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
        else:
            opts["format"] = fmt_sel
            opts["merge_output_format"] = "mp4"
            if self.subs_var.get():
                opts["writesubtitles"] = True
                opts["subtitleslangs"] = ["en"]
                opts["subtitlesformat"] = "srt"

        try:
            self.root.after(0, lambda: self.status.config(text="fetching info..."))
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
            self.root.after(0, lambda: (self.bar.config(value=100),
                                        self.status.config(text="✔ Done! Saved to " + self.folder)))
            h = load_json(HISTORY_FILE, [])
            h.insert(0, {"title": info.get("title", "?"), "url": url, "format": fmt, "folder": self.folder})
            save_json(HISTORY_FILE, h[:50])
        except Exception as e:
            self.root.after(0, lambda: self.status.config(text="Error: " + str(e)[:100]))
        finally:
            self.root.after(0, lambda: self.go_btn.config(state="normal", text="⬇  DOWNLOAD"))

if __name__ == "__main__":
    root = tk.Tk()
    DownloaderApp(root)
    root.mainloop()
