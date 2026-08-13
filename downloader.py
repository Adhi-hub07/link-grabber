"""
ADHI Downloader v3 — beautiful modern terminal app
Run:  python downloader.py        (menu)
      python downloader.py <link> [-f audio] [-o folder] [-q 1080]
"""

import os
import sys
import json
import time
import threading
import argparse
import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn, SpinnerColumn
from rich import box

try:
    import yt_dlp
except ImportError:
    raise SystemExit("[!] Run: pip install yt-dlp")

console = Console()
APP_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(APP_DIR, "config.json")
HISTORY_FILE = os.path.join(APP_DIR, "history.json")

DEFAULT_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "ADHI-HUB Downloads")

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

CONFIG = {**{"theme": "pink", "folder": DEFAULT_FOLDER},
          **load_json(CONFIG_FILE, {})}

def ensure_folder(folder):
    """Create the download folder once; reuse it after that."""
    created = not os.path.exists(folder)
    os.makedirs(folder, exist_ok=True)
    return created

THEMES = {
    "pink":   ("#ff9ec7", "#ff6fa5"),
    "blue":   ("#8fd3ff", "#5ea8ff"),
    "green":  ("#7dfa9a", "#3ddc63"),
    "sunset": ("#ffb37a", "#ff7a5e"),
    "gold":   ("#ffd97a", "#ffb347"),
}

def save_config():
    save_json(CONFIG_FILE, CONFIG)

def theme_colors():
    return THEMES.get(CONFIG["theme"], THEMES["pink"])

def theme_style():
    c1, c2 = theme_colors()
    return f"bold {c1}", f"{c2}"

def human_size(b):
    if not b: return "?"
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024: return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"

BANNER = r"""
   █████╗   ██████╗   ██╗  ██╗   ██
  ██╔══██╗  ██╔══██╗  ██║  ██║   ██
  ███████║  ██║  ██║  ███████║   ██
  ██╔══██║  ██║  ██║  ██╔══██║   ██
  ██║  ██║  ██████╔╝  ██║  ██║   ██
  ╚═╝  ╚═╝  ╚═════╝   ╚═╝  ╚═╝   ╚═
"""

TIPS = [
    "Paste links WITHOUT ?si=... for cleanest results",
    "Option 2 converts songs to MP3 automatically",
    "Playlists download in order, one after another",
    "Works with YouTube, Instagram, TikTok, Facebook + 1000 more",
    "Up to 4K quality available in the menu",
    "Subtitles download as .srt files",
    "Your history is saved — check option 7",
    "Interrupted download? It auto-resumes next time",
]

def show_menu():
    c1, c2 = theme_style()
    console.print(f"[{c1}]{BANNER}[/{c1}]")
    console.print(Panel.fit("[bold]ADHI-HUB[/bold]  —  THE ULTIMATE VIDEO & MUSIC DOWNLOADER",
                            border_style=c2, box=box.ROUNDED))
    console.print("[dim]    made with ❤ by ADHIHUB[/dim]")
    console.print(f"[dim]  {TIPS[int(time.time()) % len(TIPS)]}[/dim]\n")

    table = Table(box=box.ROUNDED, border_style=c2, pad_edge=False, title="[bold]ADHI DOWNLOADER v3[/bold]", title_style=c1)
    table.add_column("Option", style=c2, width=7)
    table.add_column("Action", style="bold white")
    table.add_column("Details", style="dim")
    rows = [
        ("1", "Download VIDEO", "best quality, you pick resolution"),
        ("2", "Download AUDIO", "auto-converts to MP3"),
        ("3", "Playlist", "downloads ALL videos in a playlist"),
        ("4", "Batch mode", "paste many links at once"),
        ("5", "Video + Subtitles", "also saves .srt captions"),
        ("6", "Settings", "change folder / theme"),
        ("7", "History", "last 50 downloads saved"),
        ("8", "About", "info about this tool"),
        ("9", "Open downloads folder", "see your downloaded files"),
        ("0", "Exit", "bye!"),
    ]
    for opt, action, detail in rows:
        table.add_row(opt, action, detail)
    console.print(table)

QUALITIES = [
    ("Best (up to 1080p)", "best"),
    ("720p", "720"),
    ("480p", "480"),
    ("2160p (4K)", "2160"),
    ("1440p (2K)", "1440"),
]

def build_opts(fmt, out_dir, quality, subs, progress):
    c1, c2 = theme_style()
    if quality != "best":
        fmt_sel = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best"
    else:
        fmt_sel = "bestvideo[height<=?1080]+bestaudio/best[height<=?1080]/best"
    opts = {
        "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
        "quiet": True, "no_warnings": True,
        "logger": ytdlp_logger(),
        "noplaylist": True,
    }
    if fmt == "audio":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
    else:
        opts["format"] = fmt_sel
        opts["merge_output_format"] = "mp4"
        if subs:
            opts["writesubtitles"] = True
            opts["subtitleslangs"] = ["en"]
            opts["subtitlesformat"] = "srt"

    task_id = [None]
    def hook(d):
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            done = d.get("downloaded_bytes", 0)
            if task_id[0] is None:
                task_id[0] = progress.add_task("", total=total)
            progress.update(task_id[0], completed=done)
    opts["progress_hooks"] = [hook]
    return opts

class ytdlp_logger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def fetch_info(url):
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "logger": ytdlp_logger(), "noplaylist": True}) as ydl:
        return ydl.extract_info(url, download=False)

def log_history(url, title, fmt, folder):
    h = load_json(HISTORY_FILE, [])
    h.insert(0, {"when": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                 "title": title, "url": url, "format": fmt, "folder": folder})
    save_json(HISTORY_FILE, h[:50])

def do_download(url, fmt, out_dir, quality="best", subs=False, playlist=False):
    c1, c2 = theme_style()
    created = ensure_folder(out_dir)
    status = "created" if created else "ready"
    console.print(f"[dim]folder: {out_dir} ({status})[/dim]")
    try:
        with console.status("[bold]fetching info...[/bold]", spinner="dots"):
            info = fetch_info(url)
        title = info.get("title", "?")
        dur = info.get("duration", 0)
        size = human_size(info.get("filesize") or info.get("filesize_approx"))
        if fmt == "audio":
            est = (dur * 192 * 1000) / 8 / 1024 / 1024  # 192kbps mp3 estimate
            size = f"~{est:.1f} MB (mp3)"

        info_table = Table(box=box.SIMPLE_HEAVY, border_style=c2)
        info_table.add_column("Info", style=c2, width=9)
        info_table.add_column("Value", style="white")
        info_table.add_row("Title", title[:64])
        if dur: info_table.add_row("Length", f"{int(dur//60)}m {int(dur%60)}s")
        info_table.add_row("Size", size)
        info_table.add_row("Mode", fmt.upper() + (" + subtitles" if subs else ""))
        info_table.add_row("Folder", out_dir)
        console.print(info_table)

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(bar_width=36), "[progress.percentage]{task.percentage:>4.1f}%",
                      TransferSpeedColumn(), TimeRemainingColumn(), console=console) as progress:
            task_id = progress.add_task(f"[{c1}]downloading[/{c1}]", total=100)
            try:
                with yt_dlp.YoutubeDL(build_opts(fmt, out_dir, quality, subs, progress)) as ydl:
                    if playlist:
                        ydl.params["noplaylist"] = False
                    ydl.download([url])
            finally:
                progress.update(task_id, completed=100)
        log_history(url, title, fmt, out_dir)
        console.print(f"[bold {c1}]✔ Done![/bold {c1}] [dim]saved to:[/dim] {out_dir}\n")
    except KeyboardInterrupt:
        console.print("[red]cancelled[/red]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)[:150]}[/red]")

def pick_quality():
    c1, c2 = theme_style()
    console.print()
    t = Table(box=box.SIMPLE, border_style=c2, show_header=False)
    for i, (name, _) in enumerate(QUALITIES, 1):
        t.add_row(f"[{c2}]{i}[/{c2}]", name)
    console.print(t)
    choice = IntPrompt.ask("[bold]quality[/bold]", default=1)
    return QUALITIES[choice - 1][1] if 1 <= choice <= len(QUALITIES) else "best"

def show_history():
    h = load_json(HISTORY_FILE, [])
    c1, c2 = theme_style()
    if not h:
        console.print("[dim]no downloads yet![/dim]")
        return
    t = Table(box=box.ROUNDED, border_style=c2, title="[bold]HISTORY[/bold]")
    t.add_column("#", style=c2, width=3)
    t.add_column("Title", style="white", width=50)
    t.add_column("Type", width=6)
    t.add_column("When", style="dim", width=16)
    for i, e in enumerate(h[:15], 1):
        t.add_row(str(i), e["title"][:48], e["format"], e["when"])
    console.print(t)

def pick_theme():
    c1, c2 = theme_style()
    console.print()
    t = Table(box=box.SIMPLE, border_style=c2, show_header=False)
    for i, name in enumerate(THEMES, 1):
        t.add_row(f"[{c2}]{i}[/{c2}]", name.title())
    console.print(t)
    choice = IntPrompt.ask("[bold]theme[/bold]", default=1)
    names = list(THEMES)
    if 1 <= choice <= len(names):
        CONFIG["theme"] = names[choice - 1]
        save_config()
        console.print(f"[{c1}]theme applied![/{c1}]")

def pick_folder():
    console.print(f"[dim]current: {CONFIG['folder']}[/dim]")
    f = Prompt.ask("[bold]new save folder[/bold]").strip()
    if f:
        CONFIG["folder"] = os.path.expanduser(f)
        save_config()
        console.print(f"[green]folder set → {CONFIG['folder']}[/green]")

def about():
    c1, c2 = theme_style()
    console.print(Panel.fit(
        "[bold]ADHI Downloader v3[/bold]\n"
        "• 1000+ supported sites (YouTube, IG, TikTok...)\n"
        "• MP4 up to 4K   •   MP3 audio   •   Subtitles\n"
        "• Playlists   •   Batch   •   History   •   Themes",
        border_style=c2, box=box.ROUNDED))

def menu():
    while True:
        show_menu()
        c = Prompt.ask("[bold]choose[/bold]")
        if c == "0":
            console.print("[bold #ff9ec7]bye! see you soon 🌸[/bold #ff9ec7]")
            break
        elif c == "1":
            url = Prompt.ask("[bold]video link[/bold]").strip()
            if url: do_download(url, "video", CONFIG["folder"], pick_quality())
        elif c == "2":
            url = Prompt.ask("[bold]song link[/bold]").strip()
            if url: do_download(url, "audio", CONFIG["folder"])
        elif c == "3":
            url = Prompt.ask("[bold]playlist link[/bold]").strip()
            if url: do_download(url, "video", CONFIG["folder"], pick_quality(), playlist=True)
        elif c == "4":
            console.print("[dim]paste links, one per line, press Enter twice:[/dim]")
            lines = []
            while True:
                line = input()
                if not line.strip(): break
                lines.append(line.strip())
            for u in lines:
                if u: do_download(u, "video", CONFIG["folder"])
        elif c == "5":
            url = Prompt.ask("[bold]video link[/bold]").strip()
            if url: do_download(url, "video", CONFIG["folder"], pick_quality(), subs=True)
        elif c == "6":
            pick_folder(); pick_theme()
        elif c == "7":
            show_history()
        elif c == "8":
            about()
        elif c == "9":
            ensure_folder(CONFIG["folder"])
            if os.name == "nt":
                os.startfile(CONFIG["folder"])
            else:
                console.print(f"[dim]your downloads are in: {CONFIG['folder']}[/dim]")
        console.print()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("url", nargs="?")
    ap.add_argument("-f", "--format", default="video")
    ap.add_argument("-o", "--output", default=CONFIG["folder"])
    ap.add_argument("-q", "--quality", default="best")
    ap.add_argument("--subs", action="store_true")
    ap.add_argument("--playlist", action="store_true")
    args = ap.parse_args()

    if args.url:
        do_download(args.url, args.format, args.output, args.quality, args.subs, args.playlist)
    else:
        menu()
