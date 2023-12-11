from pyrogram import Client, filters
from pytgcalls import PyTgCalls
import asyncio
from youtubesearchpython.__future__ import VideosSearch
from pytgcalls.types.input_stream import AudioStream
import youtube_dl
from tgmusic import pytgcalls, userbot

active_calls = {}
queue = []

async def download_song(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=True)
        return info_dict['title'], info_dict['url']

async def play_song(chat_id, query):
    try:
        title, url = await download_song(query)
    except Exception as e:
        print(f"Error downloading song: {e}")
        await userbot.send_message(chat_id, "Error downloading song.")
        return

    await userbot.send_message(chat_id, f"🔍 Searching for '{query}'. Please wait...")
    await asyncio.sleep(2)  # Simulate searching (remove this line in a real scenario)

    thumb_url = f'https://i.ytimg.com/vi/{url.split("/")[-1].split("?")[0]}/maxresdefault.jpg'
    
    await userbot.send_photo(chat_id, thumb_url,
                             caption=f"🎵 **{title}**\n🔗 [YouTube Link](https://www.youtube.com/watch?v={url.split('/')[-1].split('?')[0]})")

    group_call = pytgcalls.join_group_call(chat_id)

    try:
        audio_stream = AudioStream(
            f'https://www.youtube.com/watch?v={url.split("/")[-1].split("?")[0]}',
            codec="opus",
        )
        group_call.add_audio_stream(audio_stream)
    except Exception as e:
        print(f"Error adding audio stream: {e}")

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

async def stop_call(chat_id):
    if chat_id in active_calls:
        group_call = pytgcalls.get_group_call(chat_id)
        await group_call.leave()
        del active_calls[chat_id]

@userbot.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    await stop_call(chat_id)
    await userbot.send_message(chat_id, "🛑 Stopped playing and left the voice chat.")

@userbot.on_message(filters.command("skip"))
async def skip(client, message):
    chat_id = message.chat.id
    group_call = pytgcalls.get_group_call(chat_id)
    group_call.skip()

@userbot.on_message(filters.command("pause"))
async def pause(client, message):
    chat_id = message.chat.id
    group_call = pytgcalls.get_group_call(chat_id)
    group_call.pause_playout()

@userbot.on_message(filters.command("resume"))
async def resume(client, message):
    chat_id = message.chat.id
    group_call = pytgcalls.get_group_call(chat_id)
    group_call.resume_playout()

@userbot.on_message(filters.command("queue"))
async def show_queue(client, message):
    chat_id = message.chat.id
    if queue:
        queue_str = "\n".join([f"{i + 1}. {entry}" for i, entry in enumerate(queue)])
        await userbot.send_message(chat_id, f"**Queue:**\n{queue_str}")
    else:
        await userbot.send_message(chat_id, "Queue is empty.")

@userbot.on_message(filters.command("clear"))
async def clear_queue(client, message):
    chat_id = message.chat.id
    global queue
    queue = []
    await userbot.send_message(chat_id, "Queue cleared.")