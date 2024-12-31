from bot import bot
from datetime import datetime

# 签到记录存储：用户 ID -> {日期、签到次数、备注}
check_in_records = {}

@bot.command()
async def 簽到(ctx, message: str = ""):
    """每日簽到命令"""
    user = ctx.author
    user_name = user.display_name
    today = datetime.now().date()

    if str(user.id) in check_in_records:
        # 获取用户记录
        user_record = check_in_records[str(user.id)]
        last_date = user_record["date"]

        # 检查是否已签到
        if last_date == str(today):
            await ctx.send(f"{user_name}，你今天已经簽到過了！")
            return

        # 更新记录
        user_record["date"] = str(today)
        user_record["count"] += 1
        user_record["message"] = message
    else:
        # 新建用户记录
        check_in_records[str(user.id)] = {
            "date": str(today),
            "count": 1,
            "message": message,
        }

    await ctx.send(f"{user_name}，已成功簽到！備注：{message if message else '無'}")


@bot.command()
async def 統計(ctx,message: str = ""):
    """查看用戶簽到统計"""
    user_id = str(ctx.author.id)

    if user_id in check_in_records:
        record = check_in_records[user_id]
        await ctx.send(
            f"{ctx.author.display_name}，你累計簽到次数为: {record['count']} 次，最近簽到日期为: {record['date']}，最後備注: {record['message'] if record['message'] else '無'}"
        )
    else:
        await ctx.send(f"{ctx.author.display_name}，你還没有簽到紀錄！")


