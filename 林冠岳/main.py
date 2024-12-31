import discord
import logging
from event import on_message, on_raw_reaction_add
from 猜 import 開始終極密碼,猜,結束終極密碼
# 設定日誌級別
import logging

logging.basicConfig(level=logging.DEBUG)

from bot import bot

from event import on_message,on_raw_reaction_add,on_raw_reaction_remove
bot.add_listener(on_message, 'on_message')
bot.add_listener(on_raw_reaction_add, 'on_raw_reaction_add')
bot.add_listener(on_raw_reaction_remove, 'on_raw_reaction_remove')

# 註冊命令
from test import 簽到,統計

# 使用正確的 TOKEN 啟動機器人
bot.run("")