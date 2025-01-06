import discord
import feedparser
import logging
import google.generativeai as genai
from discord.ext import commands
from bot基本訊息 import bot  # Assuming this imports your bot object or configuration
from test import ask_bot  # Assuming you have this function in a separate file

# YouTube 頻道的 RSS URL
rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCvg7f18afqzDIRTj3VMhWkA"
last_published = None

# 設定 API 金鑰
GOOGLE_API_KEY = "AIzaSyAt5UWjPfwRQlyKDl_idjIXCrLy-BK-Bd4"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 日誌設置
logging.basicConfig(level=logging.DEBUG)

# 設定常量
MESSAGE_ID = 1301967514556694530  # 替換為需要的訊息 ID
ROLE_MAPPING_FILE = "json/role_mapping.json"  # 修改身分組的json檔案
