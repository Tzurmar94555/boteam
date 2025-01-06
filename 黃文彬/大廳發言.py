import discord
from discord.ext import commands
import json
from Bot import bot

# 全域變數
lobby_voice_channel = None
lobby_text_channel = None

# 載入玩家資料
def 讀取玩家資料():
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 機器人在大廳說話的指令
@bot.command()
async def 大廳發言(ctx, message: str):
    """直接發送消息到大廳頻道的函式"""
    global lobby_text_channel

    # 確認全域變數是否已初始化或是否有效
    if not lobby_text_channel or not discord.utils.get(ctx.guild.text_channels, id=lobby_text_channel.id):
        # 嘗試重新獲取名為 "大廳" 的文字頻道
        lobby_text_channel = discord.utils.get(ctx.guild.text_channels, name="大廳")

    # 如果找到文字頻道，發送訊息
    if lobby_text_channel:
        try:
            await lobby_text_channel.send(message)
            await ctx.send("消息已成功發送到大廳！")
        except discord.Forbidden:
            await ctx.send("機器人無法發送消息到大廳，請檢查權限設定！")
        except Exception as e:
            await ctx.send(f"發送消息時發生錯誤：{e}")
    else:
        await ctx.send("目前找不到大廳文字頻道，請先創建大廳！")



