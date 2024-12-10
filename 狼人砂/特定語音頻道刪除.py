import discord
from discord.ext import commands
from Bot import bot

@bot.command()
async def 刪除特定語音頻道(ctx,x=0):
    """刪除名稱為預言家、狼人、守衛、平民1、平民2的語音頻道"""
    # 要刪除的頻道名稱列表
    if(x==0):
        頻道名稱列表 = ["預言家", "狼人", "守衛", "平民1", "平民2"]
    if(x==1):
        頻道名稱列表 = ["大廳"]

    guild = ctx.guild  # 獲取伺服器對象
    deleted_channels = []

    # 遍歷伺服器中的語音頻道，刪除匹配名稱的頻道
    for channel in guild.voice_channels:
        if channel.name in 頻道名稱列表:
            await channel.delete(reason="清理遊戲語音頻道")
            deleted_channels.append(channel.name)

    if deleted_channels:
        await ctx.send(f"已成功刪除語音頻道：{', '.join(deleted_channels)}")
    else:
        await ctx.send("沒有找到需要刪除的語音頻道。")
