import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def send_image(ctx):
    await ctx.send(file=discord.File('path_to_your_image.jpg'))

bot.run('MTI0MTI2NTUyMDQzNTUyNzcwMA.GK1SOL.DFHtDo7pqc7g75c3mzt80EOgF1YMuZuSqlTOnU')