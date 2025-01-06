import discord
from discord.ext import commands
import json
import os
import logging
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
# 設定日誌級別
logging.basicConfig(level=logging.DEBUG)
MESSAGE_ID = 1301967514556694530 # 替換為需要的訊息 ID;修改身分組的訊息ID
ROLE_MAPPING_FILE = "json/role_mapping.json"#修改身分組的json檔案
