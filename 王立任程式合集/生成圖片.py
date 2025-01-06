import discord
from discord.ext import commands
import requests
import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取密钥
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

# 设置 Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Azure OpenAI 客户端配置
client = AzureOpenAI(
    api_version=AZURE_API_VERSION,
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT
)

# 处理 bot 启动
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 处理消息并生成图像
@bot.event
async def on_message(message):
    # 防止 bot 对自己的消息做出反应
    if message.author == bot.user:
        return

    # 如果消息是文本
    if message.content:
        prompt = message.content  # 获取用户的文本内容

        # 调用生成图像的函数
        generated_image_path = generate_image(prompt)

        # 发送生成的图像到 Discord
        with open(generated_image_path, 'rb') as image_file:
            await message.channel.send(
                content="Here is the image generated from your text:",
                file=discord.File(image_file, filename="generated_image.png")
            )

# 调用 DALL-E 生成图像
def generate_image(prompt):
    # 调用 DALL-E 生成图像
    result = client.images.generate(
        model="dall-e-3",  # the name of your DALL-E 3 deployment
        prompt=prompt,  # the prompt for generating the image
        n=1
    )

    json_response = json.loads(result.model_dump_json())

    # 设置存储图像的路径
    image_dir = os.path.join(os.curdir, 'static')  # 保存到 static 目录

    # 如果目录不存在，创建它
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # 初始化图像路径
    image_path = os.path.join(image_dir, 'generated_image.png')

    # 获取生成的图像 URL
    image_url = json_response["data"][0]["url"]
    generated_image = requests.get(image_url).content  # 下载图像

    # 将图像保存到本地
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

    return image_path  # 返回保存的图像路径

# 启动 Discord bot
bot.run(DISCORD_BOT_TOKEN)
