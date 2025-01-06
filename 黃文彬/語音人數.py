import discord
from discord.ext import commands
import json
import os
from 分配職業 import assign_random_jobs
from Bot import bot
from dotenv import load_dotenv
load_dotenv("key.env")
# 定義 player.json 的檔案路徑
player_file = 'player.json'
# 讀取 player.json 的資料，如果檔案不存在則創建
def load_player_data():
    if os.path.exists(player_file):
        with open(player_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 重設 player.json 並寫入新的資料
def reset_player_data(new_data):
    with open(player_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

@bot.event
async def on_ready():
    print(f"機器人已登入為 {bot.user}")

@bot.command()
async def 語音頻道狀態(ctx, channel_id: int):
    """偵測指定語音頻道的人數和成員資料"""
    guild = ctx.guild  # 獲取伺服器
    channel = guild.get_channel(channel_id)  # 獲取語音頻道

    if channel and isinstance(channel, discord.VoiceChannel):
        members = channel.members  # 取得語音頻道中的成員
        if members:
            # 清空 player.json 並寫入新的成員資料
            player_data = {}
            for member in members:
                # 假設你要紀錄成員的 ID、名字，並預留職業欄位
                player_data[member.id] = {
                    "name": member.name,
                    "職業": "",  # 預留職業欄位
                    "序位": members.index(member) + 1,  # 記錄成員在語音頻道中的序位
                    "狀態": "存活"  # 預設狀態為存活
                }
            reset_player_data(player_data)  # 重設並寫入新的資料

            # 回覆訊息
            member_list = [f"{member.name} (ID: {member.id})" for member in members]
            response = (
                f"語音頻道 **{channel.name}** 的成員人數：{len(members)}\n\n" +
                "\n".join(member_list)
            )
            assign_random_jobs()  # 分配隨機職業
        else:
            response = f"語音頻道 **{channel.name}** 中目前沒有成員。"
    else:
        response = "找不到該語音頻道，請確認頻道 ID 是否正確。"

    await ctx.send(response)

