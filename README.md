# 🎬 ADHI-HUB — Link Grabber

<p align="center">
  <img src="assets/banner.png" alt="ADHI-HUB Banner" width="100%">
</p>

<div align="center">

### ⬇ Direct Download (no Python needed)

[![Download TUI](https://img.shields.io/badge/⬇_Download_ADHI--HUB.exe-pink?style=for-the-badge)](https://github.com/Adhi-hub07/link-grabber/releases/download/v1.0.0/ADHI-HUB.exe)

### ⚡ One-line command (Windows PowerShell)

```powershell
irm https://github.com/Adhi-hub07/link-grabber/releases/download/v1.0.0/ADHI-HUB.exe -OutFile ADHI-HUB.exe; .\ADHI-HUB.exe
```

### 🐍 One-line install from source

```bash
pip install yt-dlp rich
```

</div>

> **The ultimate video & music downloader.** Paste a link, pick a format, done.
> Works with **YouTube, Instagram, TikTok, Facebook, Twitter** and **1000+ other sites**.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-3.0-pink)
![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-ff69b4)

</div>

---

## 📦 Which file is which?

| File | What it does | No Python needed? |
|------|--------------|-------------------|
| **`releases/ADHI-HUB.exe`** | ⭐ **Ready-made app (terminal)** — double-click, no installs | ✅ YES |
| `downloader.py` | Source code — terminal version (needs Python) | ❌ |
| `start.bat` | One-click launcher for the Python version (Windows) | ❌ |

> 💡 **Universal:** The `.exe` files run on ANY Windows PC (7/10/11) — no Python, no yt-dlp, no FFmpeg installs. Double-click and done.

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

---

## 🚀 Quick Start

### Easiest — the EXE (anyone can do this)
1. Download **`releases/ADHI-HUB.exe`**
2. Double-click it — the terminal app opens. That's it. 🎉

### From source (developers)
1. Install [Python 3](https://python.org/downloads/) (tick "Add to PATH")
2. Install dependencies:
   ```bash
   pip install yt-dlp rich
   ```
3. Run:
   ```bash
   python downloader.py
   ```
4. Or double-click **`start.bat`**

---

## 🧑‍💻 Usage

### Menu mode
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

## 📦 Requirements (source only)

| Dependency | Needed for |
|------------|------------|
| **Python 3.8+** | runs the app |
| **yt-dlp** | the download engine (`pip install yt-dlp`) |
| **rich** | beautiful terminal UI (`pip install rich`) |
| **FFmpeg** | merging video+audio and MP3 conversion |

> 💡 Tip: Paste links **without** `?si=...` for the cleanest results.

---

## 🛠️ Building the EXE yourself

```bash
pip install pyinstaller
pyinstaller --onefile --name ADHI-HUB downloader.py
```

---

## 📁 Project Structure

```
link-grabber/
├── assets/               ← banner image for README
├── releases/              ← ⭐ ready-made app, no installs needed
│   └── ADHI-HUB.exe       ← terminal version (Windows)
├── downloader.py          ← main TUI app (source)
├── start.bat              ← one-click launcher (TUI, Windows)
├── README.md
└── .gitignore
```

---

## ⚖️ License

Free to use. Built with ❤ by **ADHIHUB**.