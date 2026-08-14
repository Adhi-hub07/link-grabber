@echo off
title ADHI-HUB Bot
cd /d "%~dp0"
where ffmpeg >nul 2>nul || (
    echo [!] FFmpeg not found - MP3 downloads will fail.
    echo [*] Install it from https://ffmpeg.org or via:  winget install Gyan.FFmpeg
)
python bot.py
pause