import discord
from discord.ext import commands
import json
import os
from datetime import datetime

# 設定機器人
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 簽到記錄檔案
SIGNIN_FILE = "signin.json"

# 讀取簽到資料
def load_signins():
    if os.path.exists(SIGNIN_FILE):
        with open(SIGNIN_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# 儲存簽到資料
def save_signins(signins):
    with open(SIGNIN_FILE, "w") as file:
        json.dump(signins, file, indent=4)

# 簽到指令
@bot.command(name="signin")
async def signin(ctx):
    user_id = str(ctx.author.id)  # 使用者 ID
    signins = load_signins()

    # 檢查是否已簽到
    if user_id in signins:
        await ctx.send(f"{ctx.author.mention}，你今天已經簽到過了！")
    else:
        # 記錄簽到時間
        signins[user_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_signins(signins)
        await ctx.send(f"{ctx.author.mention}，簽到成功！")

# 查詢今日簽到
@bot.command(name="checkin")
async def checkin(ctx):
    signins = load_signins()
    today = datetime.now().strftime("%Y-%m-%d")
    signed_in_today = [member_id for member_id, signin_time in signins.items()
                       if signin_time.startswith(today)]
    
    # 顯示簽到名單
    if signed_in_today:
        members = [ctx.guild.get_member(int(member_id)).name for member_id in signed_in_today]
        await ctx.send("今天已簽到的成員：" + ", ".join(members))
    else:
        await ctx.send("今天沒有任何成員簽到。")

# 啟動機器人
@bot.event
async def on_ready():
    print(f"已登入為 {bot.user}")

# 輸入你的機器人 token
bot.run("MTI0MTI2NTUyMDQzNTUyNzcwMA.GK1SOL.DFHtDo7pqc7g75c3mzt80EOgF1YMuZuSqlTOnU")
