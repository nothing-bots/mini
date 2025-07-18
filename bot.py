import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, WEB_HOST
from youtube import YouTubeAPI

app = Client("mini-music-bot", bot_token=BOT_TOKEN)
yt = YouTubeAPI()

@app.on_message(filters.command("play") & filters.private)
async def play_song(client, message):
    if len(message.text.split()) < 2:
        return await message.reply("Usage: `/play song name`", quote=True)

    query = message.text.split(" ", 1)[1]
    track, video_id = await yt.track(query)

    url = f"{WEB_HOST}/room?t={video_id}"
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("🎧 Listen in Room", url=url)]])
    text = f"🎵 <b>{track['title']}</b>\n📺 <code>{track['link']}</code>"
    await message.reply(text, reply_markup=btn, quote=True)

if __name__ == "__main__":
    app.run()
