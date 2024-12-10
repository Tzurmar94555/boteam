import discord
import logging
from event import on_message, on_raw_reaction_add

# 設定日誌級別
import logging

logging.basicConfig(level=logging.DEBUG)

from bot import bot

from event import on_message,on_raw_reaction_add,on_raw_reaction_remove
bot.add_listener(on_message, 'on_message')
bot.add_listener(on_raw_reaction_add, 'on_raw_reaction_add')
bot.add_listener(on_raw_reaction_remove, 'on_raw_reaction_remove')

# 註冊命令
from test import 簽到

# 使用正確的 TOKEN 啟動機器人
bot.run("MTI0MTI2NTUyMDQzNTUyNzcwMA.GqUGJ9.Skeb5IlgOUhc9PxRl29vLJYZsWnIqYTQUUX6kY")