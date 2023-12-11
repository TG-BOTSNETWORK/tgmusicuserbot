from config.config import config
from pyrogram import Client
from pytgcalls import PyTgCalls


userbot = Client(
    "tgmusic",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING,
)
pytgcalls = PyTgCalls(userbot)

run = pytgcalls.start
