import asyncio
import os
import re
import shutil
import sys
import tempfile

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_token.txt")).read().strip()

MAX_SIZE = 50 * 1024 * 1024  # Telegram bot upload limit
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

BANNER = """⚡ ADHI-HUB BOT ⚡
⬇ THE ULTIMATE VIDEO & MUSIC DOWNLOADER

Send me any YouTube / Instagram / TikTok / any link,
then pick the format — I'll download it and send it back!

🔧 Commands:
/start — show this menu
/help — show this menu"""


def is_playlist(url: str) -> bool:
    return bool(re.search(r"(playlist|list=)", url, re.I))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BANNER)


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not re.match(r"https?://", url):
        return

    msg = await update.message.reply_text("🔍 Checking link...")

    try:
        with yt_dlp.YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        await msg.edit_text(f"❌ Couldn't read that link.\n`{e}`\n\nTry another link.", parse_mode="Markdown")
        return

    title = info.get("title", "Video")
    duration = int(info.get("duration") or 0)
    dur = f"{duration // 60}:{duration % 60:02d} min" if duration else "unknown length"

    keyboard = [
        [InlineKeyboardButton("🎬 MP4 Video", callback_data=f"mp4:{url}")],
        [InlineKeyboardButton("🎵 MP3 Audio (192k)", callback_data=f"mp3:{url}")],
    ]
    if is_playlist(url):
        keyboard.append([InlineKeyboardButton("📁 Whole Playlist", callback_data=f"pl:{url}")])
    keyboard.append([InlineKeyboardButton("🚫 Cancel", callback_data="cancel")])

    await msg.edit_text(
        f"🎬 **{title}**\n⏱ {dur}\n\nPick a format:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "cancel":
        await query.message.edit_text("🚫 Cancelled.")
        return

    fmt, url = data.split(":", 1)
    if fmt == "pl":
        fmt = "playlist"

    msg = await query.message.edit_text("⏳ Starting download...")

    os.makedirs(TEMP_DIR, exist_ok=True)
    workdir = tempfile.mkdtemp(dir=TEMP_DIR)

    last_progress = {"pct": 0}

    def progress_hook(d):
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes") or 0
            if total:
                pct = int(done * 100 / total)
                if pct - last_progress["pct"] >= 5:
                    last_progress["pct"] = pct
                    mb = done / 1048576
                    speed = (d.get("speed") or 0) / 1048576
                    asyncio.run_coroutine_threadsafe(
                        msg.edit_text(f"⏳ Downloading... **{pct}%** ({mb:.1f} MB, {speed:.1f} MB/s)"),
                        asyncio.get_event_loop(),
                    )

    opts = {"quiet": True, "noprogress": True, "outtmpl": os.path.join(workdir, "%(title)s.%(ext)s"), "progress_hooks": [progress_hook]}

    if fmt == "mp3":
        opts.update({"format": "bestaudio/best", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]})
    elif fmt == "mp4":
        opts.update({"format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"})
    elif fmt == "playlist":
        opts.update({"noplaylist": False, "yes_playlist": True, "format": "bestaudio/best"})

    try:
        await msg.edit_text("⏳ Downloading... **0%**")
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        await msg.edit_text(f"❌ Download failed.\n`{e}`", parse_mode="Markdown")
        shutil.rmtree(workdir, ignore_errors=True)
        return

    files = [f for f in os.listdir(workdir) if os.path.isfile(os.path.join(workdir, f))]
    if not files:
        await msg.edit_text("❌ No files found.")
        shutil.rmtree(workdir, ignore_errors=True)
        return

    big = []
    for f in files:
        path = os.path.join(workdir, f)
        if os.path.getsize(path) > MAX_SIZE:
            big.append((f, os.path.getsize(path) / 1048576))
            os.remove(path)
    if big:
        names = "\n".join(f"• {n} ({s:.1f} MB)" for n, s in big)
        await msg.edit_text(f"⚠️ Telegram's 50 MB limit — couldn't send:\n{names}\n\nTry MP3 instead. 🎵")

    remaining = [f for f in os.listdir(workdir) if os.path.isfile(os.path.join(workdir, f))]
    for f in remaining:
        path = os.path.join(workdir, f)
        title = os.path.splitext(f)[0]
        try:
            with open(path, "rb") as fh:
                if f.lower().endswith(".mp3"):
                    await msg.reply_audio(audio=fh, title=title, performer="ADHI-HUB", caption="🎵 Downloaded by ADHI-HUB Bot")
                else:
                    await msg.reply_document(document=fh, filename=f, caption="🎬 Downloaded by ADHI-HUB Bot")
        except Exception as e:
            await msg.edit_text(f"❌ Couldn't send file.\n`{e}`", parse_mode="Markdown")

    if remaining:
        await msg.edit_text("✅ **Done!** Enjoy! 🎉\nSend another link anytime.", parse_mode="Markdown")
    shutil.rmtree(workdir, ignore_errors=True)


def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(on_button))
    print("🤖 ADHI-HUB Bot is running! Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()