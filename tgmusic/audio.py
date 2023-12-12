import os
import asyncio
import ffmpeg
from os import path
from pytgcalls.types.input_stream import AudioStream, AudioParameters
from ntgcalls import InputMode
from yt_dlp import YoutubeDL
from tgmusic import pytgcalls, userbot
from pytgcalls.types.input_stream import Stream
from youtube_search import YoutubeSearch
import validators
from typing import Dict
from asyncio import Queue, QueueEmpty as Empty
from hydrogram import Client, filters

queue: Dict[int, Queue] = {}
active_calls = {}
is_playing = {}

def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

class DurationLimitError(Exception):
    pass

class FFmpegReturnCodeError(Exception):
    pass

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

async def play_song(chat_id, user_id, query):
    try:
        # Check if the query is a valid YouTube URL
        if not validators.url(query):
            # If not a URL, search for the query on YouTube
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results or not results[0].get('url_suffix') or not results[0].get('title'):
                raise Exception("No valid results found on YouTube.")

            query = f"https://youtube.com{results[0]['url_suffix']}"

        info = ydl.extract_info(query, download=False)
        title = info.get("title", "Unknown Title")
        views = info.get("view_count", "Unknown Views")
        duration = round(info.get("duration", 0) / 60)
        channel = info.get("uploader", "Unknown Channel")

        await userbot.send_message(
            chat_id,
            f"🎵Title: `{title}`\n"
            f"👀 Views: `{views}`\n"
            f"⏳ Duration: `{duration}` minutes\n"
            f"📢 Channel: `{channel}`\n"
        )

        file_path = download(query)
        raw_file = await convert(file_path)
        if chat_id not in active_calls:
            active_calls[chat_id] = user_id
            is_playing[chat_id] = True
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
            print(f"Joined group call for chat_id: {chat_id}")
        else:
            if chat_id not in queue:
                queue[chat_id] = []  

            if is_playing.get(chat_id, False):
                queue[chat_id].append(raw_file)
                await userbot.send_message(chat_id, f"🔄Title: `{title}` added to queue.")
            else:
                queue[chat_id] = [raw_file]  
                await process_queue(chat_id)  
                print(f"Processing queue for chat_id: {chat_id}")

    except DurationLimitError as de:
        print(f"Error playing song: {de}")
        await userbot.send_message(chat_id, str(de))
    except Exception as e:
        print(f"Error playing song: {e}")
        await userbot.send_message(chat_id, f"Error: {e}")

async def process_queue(chat_id):
    if chat_id in queue and len(queue[chat_id]) > 0:
        raw_file = queue[chat_id].pop(0)
        is_playing[chat_id] = True
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
        await userbot.send_message(chat_id, "▶️ Playing from queue.")
        # Recursive call to play the next song in the queue
        await process_queue(chat_id)

@userbot.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    query = " ".join(message.command[1:])
    if chat_id in active_calls:
        await play_song(chat_id, user_id, query) 
    else:
        active_calls[chat_id] = user_id
        await message.delete()
        await message.reply_text("🔍")
        await play_song(chat_id, user_id, query)

@userbot.on_message(filters.command("skip"))
async def skip(client, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    # Clear the queue when skipping
    queue[chat_id] = []
