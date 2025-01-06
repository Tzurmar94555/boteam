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

async def 移動玩家到語音大廳(guild, player_ids, lobby_voice_channel):
    """將指定的玩家移動到語音大廳"""
    for member in guild.members:
        if member.id in player_ids and member.voice:  # 玩家正在語音頻道中
            try:
                await member.move_to(lobby_voice_channel)
                print(f"已將玩家 {member.name} 移動到語音大廳")
            except Exception as e:
                print(f"無法移動玩家 {member.name}，錯誤：{e}")

@bot.command()
async def 創建大廳(ctx):
    """創建一個大廳語音頻道與文字頻道，設置權限"""
    global lobby_voice_channel, lobby_text_channel

    # 讀取玩家資料
    玩家資料 = 讀取玩家資料()
    guild = ctx.guild  # 獲取伺服器對象

    # 獲取伺服器的語音頻道和文字頻道分類
    voice_category = discord.utils.find(lambda c: c.type == discord.ChannelType.category and c.name == "語音頻道", guild.categories)
    text_category = discord.utils.find(lambda c: c.type == discord.ChannelType.category and c.name == "文字頻道", guild.categories)

    # 如果語音或文字分類不存在，創建新的分類
    if voice_category is None:
        await ctx.send("找不到預設的語音頻道分類，將創建一個新的分類。")
        voice_category = await guild.create_category("語音頻道")

    if text_category is None:
        await ctx.send("找不到預設的文字頻道分類，將創建一個新的分類。")
        text_category = await guild.create_category("文字頻道")

    # 取得 JSON 名單上的玩家 ID
    player_ids = [int(player_id) for player_id in 玩家資料.keys()]

    # 設定頻道權限，預設隱藏對所有人
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False)  # 隱藏頻道對所有人
    }

    # 設置 JSON 名單中的玩家可以查看和加入大廳
    for member in guild.members:
        if member.id in player_ids:
            overwrites[member] = discord.PermissionOverwrite(view_channel=True, connect=True, send_messages=True)

    # 創建大廳語音頻道（在語音頻道分類下）
    lobby_voice_channel = await guild.create_voice_channel(
        "大廳",
        category=voice_category,
        overwrites=overwrites
    )

    # 創建大廳文字頻道（在文字頻道分類下）
    lobby_text_channel = await guild.create_text_channel(
        "大廳",
        category=text_category,
        overwrites=overwrites
    )

    await ctx.send(f"已成功創建大廳語音與文字頻道！")

# 新增移動玩家的指令
@bot.command()
async def 移動玩家(ctx):
    """將 JSON 名單中的玩家移動到語音大廳"""
    global lobby_voice_channel
    if not lobby_voice_channel:
        await ctx.send("尚未創建大廳語音頻道，請先執行創建大廳指令！")
        return

    玩家資料 = 讀取玩家資料()
    guild = ctx.guild  # 獲取伺服器對象
    player_ids = [int(player_id) for player_id in 玩家資料.keys()]

    await 移動玩家到語音大廳(guild, player_ids, lobby_voice_channel)
    await ctx.send("已將所有名單中的玩家移動到語音大廳！")


# 刪除大廳語音頻道與文字頻道
@bot.command()
async def 刪除大廳(ctx):
    """刪除名為 '大廳' 的語音頻道與文字頻道"""
    global lobby_voice_channel, lobby_text_channel

    guild = ctx.guild

    # 刪除語音頻道
    if lobby_voice_channel:
        await lobby_voice_channel.delete()
        await ctx.send("大廳語音頻道已刪除。")
    else:
        await ctx.send("找不到名為 '大廳' 的語音頻道。")
    lobby_voice_channel = None  # 重置變數

    # 刪除文字頻道
    if lobby_text_channel:
        await lobby_text_channel.delete()
        await ctx.send("大廳文字頻道已刪除。")
    else:
        await ctx.send("找不到名為 '大廳' 的文字頻道。")
    lobby_text_channel = None  # 重置變數

