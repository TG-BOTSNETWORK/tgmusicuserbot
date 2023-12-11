from config.config import config
from pyrogram import Client
from pytgcalls import PyTgCalls


userbot = Client("tgmusic", session_string=config.STRING, api_id=config.API_ID, api_hash=config.API_HASH)
pytgcalls = PyTgCalls(userbot)

run = pytgcalls.start()
