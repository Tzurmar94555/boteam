from discord.ext import commands
from voting import VotingSession

@bot.command()
async def 投票(ctx, role):
    """開始指定角色的投票（白天/夜晚）"""
    session = VotingSession(ctx, role) 
    await session.start_voting()
