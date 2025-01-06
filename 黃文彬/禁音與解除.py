import discord
from discord.ext import commands
import json
from Bot import bot

# 載入玩家資料
def 讀取玩家資料(json_path="player.json"):
    """讀取玩家資料"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

@bot.command()
async def 禁音大廳所有人(ctx):
    """將名為 '大廳' 的語音頻道中的所有成員禁音"""
    guild = ctx.guild
    大廳 = discord.utils.get(guild.voice_channels, name="大廳")
    if not 大廳:
        await ctx.send("找不到名為 '大廳' 的語音頻道")
        return

    for member in 大廳.members:
        try:
            await member.edit(mute=True)
            await ctx.send(f"已將 {member.name} 禁音")
        except discord.Forbidden:
            await ctx.send(f"無法禁音 {member.name}，權限不足")
        except discord.HTTPException:
            await ctx.send(f"禁音 {member.name} 時發生錯誤")

    await ctx.send("所有大廳成員已禁音。")

@bot.command()
async def 解除禁音(ctx, 序位: int):
    """根據玩家序位解除禁音"""
    guild = ctx.guild
    玩家資料 = 讀取玩家資料()

    # 查找序位對應的玩家
    target_player = None
    for player_id, player_info in 玩家資料.items():
        if player_info.get("序位") == 序位:
            target_player = guild.get_member(int(player_id))
            break

    if not target_player:
        await ctx.send(f"找不到序位為 {序位} 的玩家或該玩家不在伺服器中")
        return

    try:
        await target_player.edit(mute=False)
        await ctx.send(f"已解除玩家 {target_player.name} 的禁音")
    except discord.Forbidden:
        await ctx.send(f"無法解除玩家 {target_player.name} 的禁音，權限不足")
    except discord.HTTPException:
        await ctx.send(f"解除玩家 {target_player.name} 的禁音時發生錯誤")
