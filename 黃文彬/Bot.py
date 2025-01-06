import discord
from dotenv import load_dotenv
from discord.ext import commands
# 設置 bot intents
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True
intents.members = True  # 必須啟用以讀取成員資訊
load_dotenv("key.env")
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)