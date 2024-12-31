<<<<<<< HEAD
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def send_image(ctx):
    await ctx.send(file=discord.File('https://pbs.twimg.com/media/GLCr8DEWgAACuCX.jpg:large'))

bot.run('')
=======
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def send_image(ctx):
    await ctx.send(file=discord.File('https://pbs.twimg.com/media/GLCr8DEWgAACuCX.jpg:large'))

bot.run('')
>>>>>>> 38f8ea39f1b858722c6690293cd6be5648d7e6dd
print("照片已發送")