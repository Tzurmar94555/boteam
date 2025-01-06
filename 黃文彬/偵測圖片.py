import discord
from discord.ext import commands
import os
import aiohttp
from 圖片判斷 import ask_bot_with_image
# 初始化機器人
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 設定下載的圖片存放資料夾
DOWNLOAD_FOLDER = "downloaded_images"

# 如果資料夾不存在則創建
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@bot.event
async def on_ready():
    print(f"已成功登入為 {bot.user}")

@bot.event
async def on_message(message):
    # 確保機器人不回應自己的訊息
    if message.author == bot.user:
        return

    # 檢查是否有附件
    if message.attachments:
        for attachment in message.attachments:
            # 確保附件是圖片類型
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                file_path = os.path.join(DOWNLOAD_FOLDER, attachment.filename)

                # 下載圖片
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as response:
                        if response.status == 200:
                            with open(file_path, "wb") as f:
                                f.write(await response.read())
                            x = ask_bot_with_image(file_path)
                            if "原神" in x:
                                await message.channel.send(x)
                            else:
                                await message.channel.send("555")
                            # print(f"已下載圖片：{file_path}")

                            # # 回覆使用者
                            # await message.channel.send(f"圖片已下載並儲存至：{file_path}")


