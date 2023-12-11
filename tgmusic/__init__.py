from config.config import STRING, API_ID, API_HASH
from pyrogram import Client
from pytgcalls import PyTgCalls

userbot = Client("tgmusic", session_string=STRING, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="tgmusic"))
pytgcalls = PyTgCalls(userbot)

