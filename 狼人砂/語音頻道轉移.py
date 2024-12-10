import discord
from discord.ext import commands
import json
from Bot import bot

# 載入玩家資料
def 讀取玩家資料():
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@bot.command()
async def 傳送到職業頻道(ctx):
    """根據 JSON 資料將玩家轉移到對應的職業語音頻道"""
    # 讀取玩家資料
    玩家資料 = 讀取玩家資料()
    
    guild = ctx.guild  # 獲取伺服器對象
    職業頻道 = {}  # 用於存儲職業對應的語音頻道

    # 遍歷伺服器的語音頻道，找到與職業對應的頻道
    for channel in guild.voice_channels:
        if channel.name in ["預言家", "守衛", "狼人", "平民1", "平民2"]:
            職業頻道[channel.name] = channel

    if not 職業頻道:
        await ctx.send("找不到任何職業語音頻道，請確認伺服器中已創建相關頻道。")
        return

    # 遍歷伺服器成員，將有職業的玩家移動到對應頻道
    moved_members = []
    for member in guild.members:
        player_info = 玩家資料.get(str(member.id))  # 根據玩家 ID 從 JSON 中獲取資料
        if player_info:
            職業 = player_info.get("職業")
            if 職業 and 職業 in 職業頻道:
                try:
                    await member.edit(voice_channel=職業頻道[職業])  # 移動到對應的頻道
                    moved_members.append((member.name, 職業))
                except discord.Forbidden:
                    await ctx.send(f"無法移動玩家 {member.name}，可能是權限不足。")
                except discord.HTTPException:
                    await ctx.send(f"移動玩家 {member.name} 時發生錯誤。")

    # 傳回結果
    if moved_members:
        moved_list = "\n".join([f"{name} -> {channel}" for name, channel in moved_members])
        await ctx.send(f"已成功移動以下玩家到對應頻道：\n{moved_list}")
    else:
        await ctx.send("沒有任何玩家需要移動，或找不到對應的職業頻道。")
