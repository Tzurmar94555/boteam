import discord
from discord.ext import commands
from discord.ui import Button, View
import json
from Bot import bot

# 全域變數
vote_status = {"狼人": False, "守衛": False}
vote_results = {"狼人": None, "守衛": None}

# 輔助函數
def load_player_data():
    """讀取玩家 JSON 資料"""
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_player_data(data):
    """儲存玩家 JSON 資料"""
    with open('player.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 創建職業專屬文字頻道
async def create_role_channel(guild, role):
    """創建角色專屬文字頻道"""
    channel_name = f"{role}投票區"
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    if existing_channel:
        return existing_channel

    # 設定權限
    overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}

    players = load_player_data()
    for player_id, info in players.items():
        if info["職業"] == role and info["狀態"] == "存活":
            member = guild.get_member(int(player_id))
            if member:
                overwrites[member] = discord.PermissionOverwrite(read_messages=True)

    category = discord.utils.get(guild.categories, name="文字頻道")
    if category is None:
        category = await guild.create_category("文字頻道")

    return await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)

# 按鈕處理器
class VoteButton(Button):
    def __init__(self, label, custom_id, callback):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        await self.callback_function(interaction)

class VotingSession:
    def __init__(self, ctx, role):
        self.ctx = ctx
        self.role = role
        self.players = load_player_data()
        self.votes = {}

    async def start_voting(self):
        """開始投票流程"""
        guild = self.ctx.guild
        channel = await create_role_channel(guild, self.role)
        view = View()
        for player_id, info in self.players.items():
            if info["狀態"] == "存活":
                button = VoteButton(label=f"{info['name']} ({info['序位']})",
                                    custom_id=str(player_id),
                                    callback=self.handle_vote)
                view.add_item(button)

        await channel.send(f"{self.role}請進行投票！", view=view)

    async def handle_vote(self, interaction):
        """處理投票邏輯"""
        voter_id = str(interaction.user.id)
        if voter_id not in self.players:
            await interaction.response.send_message("你不在投票名單中！", ephemeral=True)
            return

        if voter_id in self.votes:
            await interaction.response.send_message("你已經投過票了！", ephemeral=True)
            return

        target_id = interaction.data['custom_id']
        self.votes[voter_id] = target_id

        await interaction.response.send_message(f"你已投票給 {self.players[target_id]['name']}！", ephemeral=True)

        if len(self.votes) == len([p for p in self.players.values() if p["狀態"] == "存活" and p["職業"] == self.role]):
            await self.end_voting()

    async def end_voting(self):
        """結束投票並處理結果"""
        global vote_status, vote_results

        if self.role == "守衛":
            vote_results["守衛"] = {voter: target for voter, target in self.votes.items()}
            vote_status["守衛"] = True
        elif self.role == "狼人":
            vote_counts = {}
            for target in self.votes.values():
                vote_counts[target] = vote_counts.get(target, 0) + 1

            max_votes = max(vote_counts.values())
            potential_victims = [player for player, votes in vote_counts.items() if votes == max_votes]

            import random
            victim = random.choice(potential_victims) if len(potential_victims) > 1 else potential_victims[0]
            vote_results["狼人"] = victim
            vote_status["狼人"] = True
        elif self.role == "預言家":
            await self.handle_seer_result()

        # 若狼人與守衛的投票均已完成，處理最終結果
        if vote_status["狼人"] and vote_status["守衛"]:
            await handle_combined_results(self.ctx.guild)

    async def handle_seer_result(self):
        """處理預言家的投票結果"""
        global vote_results

        # 獲取預言家的投票目標
        target_id = list(self.votes.values())[0]
        players = load_player_data()
        target_info = players[target_id]

        # 判斷目標是否為狼人
        result_message = f"{target_info['name']} 是 {'狼人' if target_info['職業'] == '狼人' else '非狼人'}。"

        # 傳送結果至預言家的專屬頻道
        guild = self.ctx.guild
        seer_channel = discord.utils.get(guild.text_channels, name="預言家投票區")
        if seer_channel:
            await seer_channel.send(result_message)

        # 標記預言家投票完成
        vote_status["預言家"] = True

@bot.command()
async def 投票(ctx):
    """為存活的狼人、預言家、守衛創建專屬文字頻道並開始投票"""
    guild = ctx.guild
    players = load_player_data()

    roles_to_create = ["狼人", "預言家", "守衛"]
    for role in roles_to_create:
        # 確認是否有該職業且存活的玩家
        has_alive_player = any(info["職業"] == role and info["狀態"] == "存活" for info in players.values())
        if not has_alive_player:
            # 如果守衛已死亡，標記投票完成
            if role == "守衛":
                global vote_status
                vote_status["守衛"] = True
            continue

        # 創建專屬頻道並啟動投票
        await create_role_channel(guild, role)
        session = VotingSession(ctx, role)
        await session.start_voting()

    await ctx.send("已為存活的狼人、預言家、守衛創建對應的頻道並開始投票。")



async def handle_combined_results(guild):
    """處理狼人和守衛投票的最終結果"""
    global vote_results, vote_status

    players = load_player_data()

    # 如果守衛已死亡或沒投票，直接跳過守衛邏輯
    wolf_target_id = vote_results["狼人"]
    guard_target_id = vote_results["守衛"]
    guard_target_id = None if guard_target_id is None else list(guard_target_id.values())[0]

    if guard_target_id and wolf_target_id == guard_target_id:
        result_message = f"守衛成功保護了 {players[wolf_target_id]['name']}！"
    else:
        if wolf_target_id:
            players[wolf_target_id]["狀態"] = "死亡"
            result_message = f"{players[wolf_target_id]['name']} 被狼人攻擊，已死亡！"
        else:
            result_message = "狼人沒有攻擊任何人。"

    save_player_data(players)

    # 傳送結果到頻道
    wolf_channel = discord.utils.get(guild.text_channels, name="狼人投票區")
    guard_channel = discord.utils.get(guild.text_channels, name="守衛投票區")
    if wolf_channel:
        await wolf_channel.send(result_message)
    if guard_channel:
        await guard_channel.send(result_message)

    # 重置投票狀態
    vote_status = {"狼人": False, "守衛": False}
    vote_results = {"狼人": None, "守衛": None}