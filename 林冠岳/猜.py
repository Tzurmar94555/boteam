from bot import bot
import random

# 存储终极密码游戏的状态
ultimate_password_game = {}

@bot.command()
async def 開始終極密碼(ctx):
    """開始终极密碼游戏"""
    if ctx.channel.id in ultimate_password_game:
        await ctx.send("遊戲已经在進行中了！使用 `!結束終極密碼` 结束當前遊戲。")
        return

    # 初始化游戏状态
    secret_number = random.randint(1, 100)
    ultimate_password_game[ctx.channel.id] = {
        "secret": secret_number,
        "min": 1,
        "max": 100,
        "attempts": 0,
    }
    await ctx.send("终級密碼遊戲開始！我已選擇了 1 到 100 之間的一個數字，來猜猜看吧！")

@bot.command()
async def 猜(ctx, number: int):
    """猜测终极密码"""
    if ctx.channel.id not in ultimate_password_game:
        await ctx.send("目前没有進行中的终級密碼遊戲。使用 `!開始終極密碼` 開始一局新遊戲！")
        return

    # 获取当前游戏状态
    game_state = ultimate_password_game[ctx.channel.id]
    secret_number = game_state["secret"]
    min_val = game_state["min"]
    max_val = game_state["max"]
    game_state["attempts"] += 1

    # 检查猜测
    if number < min_val or number > max_val:
        await ctx.send(f"無效的數字！請猜測 {min_val} 到 {max_val} 之間的數字。")
    elif number < secret_number:
        game_state["min"] = max(min_val, number + 1)
        await ctx.send(f"更大！請猜測 {game_state['min']} 到 {max_val} 之間的數字。")
    elif number > secret_number:
        game_state["max"] = min(max_val, number - 1)
        await ctx.send(f"更小！請猜測 {min_val} 到 {game_state['max']} 之間的數字。")
    else:
        # 猜对了，游戏结束
        attempts = game_state["attempts"]
        await ctx.send(f"恭喜，{ctx.author.display_name}！在 {attempts} 次猜測後找到了秘密數字：{secret_number}！")
        del ultimate_password_game[ctx.channel.id]

@bot.command()
async def 結束終極密碼(ctx):
    """结束當前的終級密碼游戏"""
    if ctx.channel.id not in ultimate_password_game:
        await ctx.send("目前没有進行中的終級密碼遊戲。")
        return

    # 删除游戏状态
    del ultimate_password_game[ctx.channel.id]
    await ctx.send("當前的终級密碼遊戲已结束！歡迎随時重新開始。")
