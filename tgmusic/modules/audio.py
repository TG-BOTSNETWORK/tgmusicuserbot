from pyrogram import Client, filters
from pytgcalls import PyTgCalls
import asyncio
from youtubesearchpython.__future__  import VideosSearch
from pytgcalls.types.input_stream import AudioStream
from tgmusic import pytgcalls, userbot

active_calls = {}

async def play_song(chat_id, query):
    videosSearch = VideosSearch(query, limit=1)
    results = videosSearch.result()
    if not results["result"]:
        await userbot.send_message(chat_id, "No results found for your query.")
        return

    video_info = results["result"][0]

    thumb_url = video_info["thumbnails"][0]["url"]
    song_name = video_info["title"]
    views = video_info["viewCount"]["short"]
    duration = video_info["duration"]
    channel_name = video_info["channel"]["name"]

    await userbot.send_photo(chat_id, thumb_url,
                         caption=f"🎵 **{song_name}**\n👤 {channel_name}\n👁️ {views} views\n⏱️ {duration}")

    group_call = pytgcalls.join_group_call(chat_id)

    try:
        audio_stream = group_call.AudioStream(
            f'https://www.youtube.com/watch?v={video_info["id"]}',
            codec="opus",
        )
        group_call.add_audio_stream(audio_stream)
    except Exception as e:
        print(f"Error adding audio stream: {e}")

@Client.on_message(filters.command("play"))
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
        await message.reply_text(chat_id, "Bot is currently busy in another chat. Try again later.")

async def stop_call(chat_id):
    if chat_id in active_calls:
        group_call = pytgcalls.get_group_call(chat_id)
        await group_call.leave()
        del active_calls[chat_id]

@Client.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    await stop_call(chat_id)
    await userbot.send_message(chat_id, "🛑 Stopped playing and left the voice chat.")
