import discord
from discord.ext import commands
import json
import os
from bot import bot

MESSAGE_ID = 1301967514556694530 # 替換為需要的訊息 ID

async def on_message(message):
    if message.author == message.guild.me:
        return  # 忽略機器人自己的訊息

    if "早安" in message.content and message.content[0] != "!":
        await message.channel.send("早安")

async def on_raw_reaction_add(payload):
    if payload.message_id == MESSAGE_ID: #接收到的訊息ID
        print("接收到訊息")
        channel = bot.get_channel(payload.channel_id)
        await channel.send("已經加入了表情符號")

async def on_raw_reaction_remove(payload):
    if payload.message_id == MESSAGE_ID:
        channel = bot.get_channel(payload.channel_id)
        await channel.send("已經移除了表情符號")
    
