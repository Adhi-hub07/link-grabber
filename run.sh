#!/bin/bash
# ADHI-HUB Link Grabber — Linux/macOS launcher
cd "$(dirname "$0")"

# check python
if ! command -v python3 &>/dev/null; then
    echo "[!] Python 3 is not installed. Install it first:  sudo apt install python3"
    exit 1
fi

# install dependencies if missing
python3 -c "import yt_dlp" 2>/dev/null || pip3 install --user yt-dlp rich 2>/dev/null || pip3 install yt-dlp rich

python3 downloader.py