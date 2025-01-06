import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取密钥
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 设置 Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 加载扩展 (cogs)
bot.load_extension("cogs.image_generator")

# 处理 bot 启动
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 启动 Discord bot
bot.run(DISCORD_BOT_TOKEN)
