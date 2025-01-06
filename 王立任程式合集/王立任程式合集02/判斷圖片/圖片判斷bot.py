import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.azure_utils import AzurePredictor

# 加載 .env 文件中的變數
load_dotenv()

# 從環境變數中獲取敏感資訊
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 設定 Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 初始化 Azure Custom Vision 預測器
azure_predictor = AzurePredictor()

# 當 bot 準備好時的回應
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

# 處理圖片上傳並進行預測
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                response = await azure_predictor.handle_image(attachment)
                await message.channel.send(response)

    await bot.process_commands(message)

# 啟動 bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
