from bot import bot
import discord
check_in_records = {}
@bot.command()
async def 簽到(ctx,channel_id:int = ""): #ctx 是機器人(一定要是ctx)在這個函式中的代稱; teach改成你想要的指令名稱
    """偵測指定語音頻道的人數和成員資料"""
    guild = ctx.guild  # 獲取伺服器
    channel = guild.get_channel(channel_id)  # 獲取語音頻道
    print("test")
    if channel and isinstance(channel, discord.VoiceChannel):
        members = channel.members  # 取得語音頻道中的成員
        if members:
            member_list = [f"{member.name} (ID: {member.id})" for member in members]
            response = (
                f"語音頻道 **{channel.name}** 的成員人數：{len(members)}\n\n" +
                "\n".join(member_list)
            )
        else:
            response = f"語音頻道 **{channel.name}** 中目前沒有成員。"
    else:
        response = "找不到該語音頻道，請確認頻道 ID 是否正確。"

    await ctx.send(response)
    # user = ctx.author  # 获取发送命令的用户
    # user_name = user.display_name  # 获取用户的 Discord 名称
    # if user.id in check_in_records:
    #     await ctx.send(f"{user_name}，你今天已经签到过了！")
    # else:
    #     # 将用户记录为已签到
    #     check_in_records[user.id] = user_name
    #     await ctx.send(f"{user_name}，已成功签到！")
