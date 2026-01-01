from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

TOKEN = "8546466962:AAEZ3w7OuldtOWfS38fAvrGTOUy8VA9aegQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌊 Welcome to CIZED WAVE\n\nUse /search song name"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🎵 Write song name after /search")
        return

    query = " ".join(context.args)
    context.user_data["last_search"] = query

    await update.message.reply_text(
        f"🔍 Found: {query}\n\nUse /download to get the song"
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = context.user_data.get("last_search")

    if not query:
        await update.message.reply_text("❌ First use /search")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    await update.message.reply_text("⏳ Downloading...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])

    await update.message.reply_audio(
        audio=open("song.mp3", "rb"),
        title=query
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("download", download))

app.run_polling()
