from bot import bot
@bot.command()
async def teach(ctx,message:str = "",message2:str = ""): #ctx 是機器人(一定要是ctx)在這個函式中的代稱; teach改成你想要的指令名稱
    if message == "" and message2 == "":
        await ctx.send("請輸入內容")
    else:
        await ctx.send(f"{message}{message2}")#send 是讓機器人發送訊息的函式