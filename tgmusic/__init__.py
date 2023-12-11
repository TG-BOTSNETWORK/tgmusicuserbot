from config.config import STRING, API_ID, API_HASH
from pyrogram import Client
from pytgcalls import PyTgCalls

userbot = Client(STRING, api_id=config.API_ID, api_hash=config.API_HASH, plugins=dict(root="tgmusic"))
pytgcalls = PyTgCalls(userbot)

