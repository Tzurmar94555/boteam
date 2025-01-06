import discord
from discord.ext import commands

# 設定 Bot 的 Intent
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

# 設定 Bot
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
