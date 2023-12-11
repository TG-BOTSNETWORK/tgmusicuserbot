from config.config import config
from pyrogram import Client
from pytgcalls import PyTgCalls


userbot = Client(config.STRING, api_id=config.API_ID, api_hash=config.API_HASH, plugins=dict(root="tgmusic")
pytgcalls = PyTgCalls(userbot)

