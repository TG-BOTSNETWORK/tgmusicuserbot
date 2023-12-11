from tgmusic import pytgcalls, userbot
from pyrogram import idle
from pytgcalls import idle as tgidle

if __name__ == "__main__":
   userbot.start()
   print("UserBot Started")
   pytgcalls.start()
   print("Vc Client Started")
   tgidle()
   idle()
    
