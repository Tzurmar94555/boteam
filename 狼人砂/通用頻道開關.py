import discord
from discord.ext import commands
import json
from Bot import bot

# 讀取玩家資料
def 讀取玩家資料(json_path="player.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 開關 player.json 玩家特定頻道的查看權限
@bot.command()
async def 切換玩家頻道可見(ctx, 狀態: str):
    """
    將 player.json 中的玩家設置為無法查看或恢復查看所有頻道（不改變 @everyone 的權限）。
    狀態: "開" 或 "關"
    """
    if 狀態 not in ["開", "關"]:
        await ctx.send("請輸入正確的狀態：開 或 關")
        return

    guild = ctx.guild
    玩家資料 = 讀取玩家資料()
    玩家_ids = [int(player_id) for player_id in 玩家資料.keys()]  # 從 JSON 獲取玩家 ID

    成功玩家 = []
    失敗玩家 = []

    # 遍歷所有頻道
    for channel in guild.channels:
        if any(keyword in channel.name for keyword in ["狼人殺", "大廳", "守衛", "村民", "預言家", "狼人"]):
            continue  # 忽略與狼人殺相關的頻道


        for member in guild.members:
            if member.id in 玩家_ids:
                try:
                    if 狀態 == "關":
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(view_channel=False))
                    elif 狀態 == "開":
                        await channel.set_permissions(member, overwrite=None)  # 恢復玩家的預設權限
                    成功玩家.append(member.name)
                except Exception as e:
                    失敗玩家.append((member.name, channel.name, str(e)))

    # 結果回報
    if 成功玩家:
        await ctx.send(f"已成功設置頻道權限為 '{狀態}' 給以下玩家：\n" + ", ".join(set(成功玩家)))
    if 失敗玩家:
        await ctx.send("以下玩家在指定頻道的權限設置失敗：\n" + "\n".join([f"{name} @ {channel} -> {error}" for name, channel, error in 失敗玩家]))
