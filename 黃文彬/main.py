import os
from Bot import bot
from 狼人殺 import 開始遊戲
from 偵測圖片 import *
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)