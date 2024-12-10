import discord
from discord.ext import commands
import json
from Bot import bot
from 語音頻道轉移 import 傳送到職業頻道
# 載入玩家資料
def 讀取玩家資料():
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 創建語音頻道並設定權限
@bot.command()
async def 創建職業語音頻道(ctx):
    """為每個職業創建語音頻道，並設置權限，讓對應職業玩家能查看和加入"""
    # 讀取玩家資料
    玩家資料 = 讀取玩家資料()

    guild = ctx.guild  # 獲取伺服器對象

    # 獲取伺服器的語音頻道分類
    category = discord.utils.find(lambda c: c.type == discord.ChannelType.category and c.name == "語音頻道", guild.categories)
    if category is None:
        await ctx.send("找不到預設的語音頻道分類，將創建一個新的分類。")
        category = await guild.create_category("語音頻道")

    # 以職業為鍵分組玩家
    職業_to_players = {}
    for player_id, data in 玩家資料.items():
        職業 = data["職業"]
        if 職業 not in 職業_to_players:
            職業_to_players[職業] = []
        職業_to_players[職業].append(int(player_id))  # 將玩家 ID 存入該職業的列表

    # 為每個職業創建語音頻道
    for 職業, player_ids in 職業_to_players.items():
        # 設定頻道權限，預設隱藏對所有人
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False)  # 隱藏頻道對所有人
        }

        # 設置該職業的玩家可以查看和加入頻道
        for member in guild.members:
            if member.id in player_ids:
                overwrites[member] = discord.PermissionOverwrite(view_channel=True, connect=True)

        # 創建語音頻道
        new_channel = await guild.create_voice_channel(
            職業,
            category=category,
            overwrites=overwrites
        )

        await ctx.send(f"已成功創建語音頻道 '{職業}'，並設置權限。")
        await 傳送到職業頻道(ctx)  # 移動玩家到對應職業頻道

    await ctx.send("所有職業語音頻道已成功創建！")
