from config.config import config
from pyrogram import Client
from pytgcalls import PyTgCalls


userbot = Client(config.STRING, config.API_ID, config.API_HASH)
pytgcalls = PyTgCalls(userbot)

run = pytgcalls.start
