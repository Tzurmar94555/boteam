import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# 加載 .env 文件中的變數
load_dotenv()

# 從環境變數中獲取敏感資訊
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AZURE_PREDICTION_KEY = os.getenv("AZURE_PREDICTION_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_PROJECT_ID = os.getenv("AZURE_PROJECT_ID")
AZURE_ITERATION_NAME = os.getenv("AZURE_ITERATION_NAME")

# Azure Custom Vision 配置
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": AZURE_PREDICTION_KEY})
predictor = CustomVisionPredictionClient(AZURE_ENDPOINT, prediction_credentials)

# 設定 Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 當 bot 準備好時的回應
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

# 處理圖片上傳並進行預測
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 檢查是否有附件（圖片）
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                # 下載圖片
                image_bytes = await attachment.read()

                # 調用 Azure Custom Vision 進行預測
                try:
                    results = predictor.classify_image(AZURE_PROJECT_ID, AZURE_ITERATION_NAME, image_bytes)

                    # 找出最高機率的標籤
                    top_prediction = max(results.predictions, key=lambda p: p.probability)

                    # 只關注貓和狗，且預測機率必須大於 0.9
                    if top_prediction.tag_name.lower() in ["cat", "dog"] and top_prediction.probability >= 0.9:
                        predicted_label = top_prediction.tag_name
                        await message.channel.send(f"這張圖片是 {predicted_label}")
                    else:
                        await message.channel.send("這張圖片既不是貓也不是狗")

                except Exception as e:
                    await message.channel.send(f"處理圖片時發生錯誤: {e}")

    await bot.process_commands(message)

# 啟動 bot
bot.run(DISCORD_TOKEN)
