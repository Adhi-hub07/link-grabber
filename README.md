# 🎬 ADHI-HUB — The Ultimate Video & Music Downloader

> **ADHI-HUB** — The ultimate video & music downloader. Paste a link, pick a format, done.
> Works with **YouTube, Instagram, TikTok, Facebook, Twitter** and **1000+ other sites**.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-3.0-pink)
![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-ff69b4)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎥 **Video download** | MP4 up to **4K**, pick your resolution (480p / 720p / 1080p / 2K / 4K) |
| 🎵 **Audio download** | Auto-converts to **MP3** (192 kbps) |
| 📃 **Playlists** | Download an entire playlist at once |
| 📦 **Batch mode** | Paste many links, download them all |
| 💬 **Subtitles** | Save `.srt` captions alongside the video |
| 🕘 **History** | Your last 50 downloads, stored locally |
| 🎨 **Themes** | 5 color themes: Pink, Blue, Green, Sunset, Gold |
| 📊 **Live progress** | Animated progress bar with speed + ETA |
| 🖥️ **GUI version** | Bonus clickable window app (no terminal needed) |

---

## 🚀 Quick Start (Windows)

### Option A — Just run it
1. Install [Python 3](https://python.org/downloads/) (tick "Add to PATH")
2. Open a terminal in the project folder and run:
   ```bash
   pip install yt-dlp rich
   ```
3. Double-click **`start.bat`** — or run:
   ```bash
   python downloader.py
   ```

### Option B — GUI (easier)
Double-click **`start_gui.bat`**, or run:
```bash
python downloader_gui.py
```

---

## 🧑‍💻 Usage

### Menu mode
Run the program, pick an option, paste your link:

```
1)  Download VIDEO          ← pick quality: 480p → 4K
2)  Download AUDIO (mp3)    ← auto-converts
3)  Download PLAYLIST       ← every video in the list
4)  Batch mode              ← many links at once
5)  Video + Subtitles       ← also saves .srt
6)  Settings                ← folder / theme
7)  History                 ← last 50 downloads
8)  About
0)  Exit
```

### Command line (fast)
```bash
python downloader.py "https://youtu.be/abc123"          # video, best quality
python downloader.py "LINK" -f audio                     # MP3 only
python downloader.py "LINK" -f video -q 2160             # 4K video
python downloader.py "LINK" -o "D:/Videos"               # custom folder
python downloader.py "LINK" --subs                       # with subtitles
python downloader.py "PLAYLIST_LINK" --playlist          # whole playlist
```

---

## 📦 Requirements

| Dependency | Needed for |
|------------|------------|
| **Python 3.8+** | runs the app |
| **yt-dlp** | the download engine (`pip install yt-dlp`) |
| **rich** | beautiful terminal UI (`pip install rich`) |
| **FFmpeg** | merging video+audio and MP3 conversion |

> 💡 Tip: Paste links **without** `?si=...` for the cleanest results.

---

## 📁 Project Structure

```
adhi-hub-downloader/
├── downloader.py        ← main TUI app
├── downloader_gui.py    ← GUI version
├── start.bat            ← one-click launcher (TUI)
├── start_gui.bat        ← one-click launcher (GUI)
├── config.json          ← your settings (created on first run)
└── history.json         ← your download history (created on first run)
```

---

## ⚖️ License

Free to use. Built with ❤ by **ADHIHUB**.