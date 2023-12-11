from tgmusic import pytgcalls, userbot
from hydrogram import idle
from pytgcalls import idle as tgidle

if __name__ == "__main__":
   userbot.start()
   print("[USER BOT STARTED] - IMPORTED ALL PLUGINS FROM TGMUSIC.")
   pytgcalls.start()
   print("[VOICE CHAT STARTED] - VOICE CHARTED STARTED!")
   tgidle()
   idle()
    
