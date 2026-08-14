<p align="center">
  <img src="assets/banner.png" alt="ADHI-HUB Banner" width="100%">
</p>

<div align="center">

# 🎬 ADHI-HUB — Link Grabber

**The ultimate video & music downloader.** Paste a link → pick format → done.
Works with **YouTube, Instagram, TikTok, Facebook, Twitter** and **1000+ other sites**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-3.0-pink)
![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-ff69b4)

</div>

---

## 🚀 Quick Start

### Option A — EXE (easiest, for everyone)

No Python. No installs. Just download & double-click.

[![Download EXE](https://img.shields.io/badge/⬇_Download_ADHI--HUB.exe-pink?style=for-the-badge)](https://github.com/Adhi-hub07/link-grabber/releases/download/v1.0.0/ADHI-HUB.exe)

**One-line command (Windows PowerShell):**
```powershell
irm https://github.com/Adhi-hub07/link-grabber/releases/download/v1.0.0/ADHI-HUB.exe -OutFile ADHI-HUB.exe; .\ADHI-HUB.exe
```

### Option B — Python source (for developers)

[![Download start.bat](https://img.shields.io/badge/⬇_Download_start.bat-8fd3ff?style=for-the-badge)](https://raw.githubusercontent.com/Adhi-hub07/link-grabber/main/start.bat)

```bash
pip install yt-dlp rich
python downloader.py
```

### Option C — Linux / macOS 🐧

[![Download run.sh](https://img.shields.io/badge/⬇_Download_run.sh-7dfa9a?style=for-the-badge)](https://raw.githubusercontent.com/Adhi-hub07/link-grabber/main/run.sh)

```bash
chmod +x run.sh
./run.sh
```

Or grab the pre-built **`ADHI-HUB-linux`** binary from the [latest release](https://github.com/Adhi-hub07/link-grabber/releases).

---

## 📦 Which file is which?

| File | What it does | Needs Python? |
|------|--------------|---------------|
| `releases/ADHI-HUB.exe` | ⭐ Ready-made app — works on any Windows PC, double-click and done | ❌ No |
| `ADHI-HUB-linux` | ⭐ Ready-made app — for Linux (from releases) | ❌ No |
| `downloader.py` | Source code — the app itself (Windows / Linux / macOS) | ✅ Yes |
| `start.bat` | One-click launcher — Windows | ✅ Yes |
| `run.sh` | One-click launcher — Linux / macOS | ✅ Yes |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎥 **Video download** | MP4 up to **4K** — pick 480p / 720p / 1080p / 2K / 4K |
| 🎵 **Audio download** | Auto-converts to **MP3** (192 kbps) |
| 📃 **Playlists** | Download an entire playlist at once |
| 📦 **Batch mode** | Paste many links, download them all |
| 💬 **Subtitles** | Saves `.srt` captions with the video |
| 🕘 **History** | Last 50 downloads, stored locally |
| 🎨 **Themes** | 5 colors: Pink, Blue, Green, Sunset, Gold |
| 📊 **Live progress** | Animated bar + speed + ETA |
| 📁 **Smart folder** | Auto-creates `ADHI-HUB Downloads` — all files in one place |

---

## 🧑‍💻 Usage

### Menu mode
```
1)  Download VIDEO           ← pick quality: 480p → 4K
2)  Download AUDIO (mp3)     ← auto-converts
3)  Download PLAYLIST        ← every video in the list
4)  Batch mode               ← many links at once
5)  Video + Subtitles        ← also saves .srt
6)  Settings                 ← folder / theme
7)  History                  ← last 50 downloads
8)  About
9)  Open downloads folder    ← see your files
0)  Exit
```

### Command line (fast)
```bash
python downloader.py "https://youtu.be/abc123"       # video, best quality
python downloader.py "LINK" -f audio                  # MP3 only
python downloader.py "LINK" -f video -q 2160          # 4K video
python downloader.py "LINK" -o "D:/Videos"            # custom folder
python downloader.py "LINK" --subs                    # with subtitles
python downloader.py "PLAYLIST_LINK" --playlist       # whole playlist
```

---

## 📦 Requirements (source only)

| Dependency | Needed for |
|------------|------------|
| **Python 3.8+** | runs the app |
| **yt-dlp** | the download engine |
| **rich** | beautiful terminal UI |
| **FFmpeg** | merging video + audio, MP3 conversion |

> 💡 **Tip:** Paste links **without** `?si=...` for the cleanest results.

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
├── assets/             ← banner image for README
├── releases/           ← ⭐ ready-made app (ADHI-HUB.exe)
├── downloader.py       ← main app (source — works on all systems)
├── start.bat           ← Windows launcher
├── run.sh              ← Linux / macOS launcher
├── README.md
└── .gitignore
```

---

## ⚖️ License

**MIT** — free to use, share and modify. Built with ❤ by **ADHIHUB**.