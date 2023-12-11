import os
import asyncio
import ffmpeg
from os import path
from pytgcalls.types.input_stream import AudioStream, AudioParameters
from ntgcalls import InputMode
from yt_dlp import YoutubeDL
from tgmusic import pytgcalls, userbot
from hydrogram import Client, filters
from pytgcalls.types.input_stream import Stream
from youtube_search import YoutubeSearch
import validators

class DurationLimitError(Exception):
    pass

class FFmpegReturnCodeError(Exception):
    pass

active_calls = {}
queue = []

DURATION_LIMIT = 60

ydl_opts = {
    "format": "bestaudio/best",
    "verbose": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)

def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )

    ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")

async def play_song(chat_id, query):
    try:
        # Check if the query is a valid YouTube URL
        if not validators.url(query):
            # If not a URL, search for the query on YouTube
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results:
                raise Exception("No results found on YouTube.")
            query = f"https://youtube.com{results[0]['url_suffix']}"

        info = ydl.extract_info(query, download=False)
        title = info.get("title", "Unknown Title")
        views = info.get("view_count", "Unknown Views")
        duration = round(info.get("duration", 0) / 60)
        channel = info.get("uploader", "Unknown Channel")

        await userbot.send_message(
            chat_id,
            f"🎵 **{title}**\n"
            f"👀 Views: {views}\n"
            f"⏳ Duration: {duration} minutes\n"
            f"📢 Channel: {channel}\n"
            f"🔗 [YouTube Link]({query})",
        )

        file_path = download(query)

        # Convert the audio file
        raw_file = await convert(file_path)

        await pytgcalls.join_group_call(
            chat_id,
            Stream(
                AudioStream(
                    input_mode=InputMode.File,
                    path=raw_file,
                    parameters=AudioParameters(
                        bitrate=48000,
                        channels=1
                    )
                )
            )
        )

    except Exception as e:
        print(f"Error playing song: {e}")
        await userbot.send_message(chat_id, f"Error playing song: {e}")

@userbot.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    query = " ".join(message.command[1:])

    if chat_id not in active_calls:
        active_calls[chat_id] = user_id
        await message.delete()
        await message.reply_text("🔍")
        await play_song(chat_id, query)
    else:
        await userbot.send_message(chat_id, "Bot is currently busy in another chat. Try again later.")

# Rest of your code...

async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 1 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    if proc.returncode != 0:
        raise FFmpegReturnCodeError("FFmpeg did not return 0")

    return out
