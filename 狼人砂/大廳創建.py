import discord
from discord.ext import commands
import json
from Bot import bot

# 載入玩家資料
def 讀取玩家資料():
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 創建大廳並設置權限，並將 JSON 名單中的玩家移動到大廳
@bot.command()
async def 創建大廳(ctx):
    """創建一個大廳語音頻道，設置權限，並將 JSON 名單中的玩家移動到大廳"""
    # 讀取玩家資料
    玩家資料 = 讀取玩家資料()

    guild = ctx.guild  # 獲取伺服器對象

    # 獲取伺服器的語音頻道分類
    category = discord.utils.find(lambda c: c.type == discord.ChannelType.category and c.name == "語音頻道", guild.categories)
    if category is None:
        await ctx.send("找不到預設的語音頻道分類，將創建一個新的分類。")
        category = await guild.create_category("語音頻道")

    # 取得 JSON 名單上的玩家 ID
    player_ids = [int(player_id) for player_id in 玩家資料.keys()]

    # 設定頻道權限，預設隱藏對所有人
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False)  # 隱藏頻道對所有人
    }

    # 設置 JSON 名單中的玩家可以查看和加入大廳
    for member in guild.members:
        if member.id in player_ids:
            overwrites[member] = discord.PermissionOverwrite(view_channel=True, connect=True)

    # 創建大廳語音頻道
    lobby_channel = await guild.create_voice_channel(
        "大廳",
        category=category,
        overwrites=overwrites
    )

    # 將 JSON 名單中的玩家移動到大廳
    for member in guild.members:
        if member.id in player_ids and member.voice:  # 玩家正在語音頻道中
            try:
                await member.move_to(lobby_channel)
                print(f"已將玩家 {member.name} 移動到大廳")
            except Exception as e:
                print(f"無法移動玩家 {member.name}，錯誤：{e}")

    await ctx.send(f"已成功創建大廳語音頻道，並將所有名單中的玩家移動到大廳！")

# 刪除大廳語音頻道
@bot.command()
async def 刪除大廳(ctx):
    """刪除名為 '大廳' 的語音頻道"""
    guild = ctx.guild  # 獲取伺服器對象
    lobby_channel = discord.utils.get(guild.voice_channels, name="大廳")  # 查找名為 '大廳' 的語音頻道
    if lobby_channel:
        await lobby_channel.delete()
        await ctx.send("大廳語音頻道已刪除。")
    else:
        await ctx.send("找不到名為 '大廳' 的語音頻道。")
