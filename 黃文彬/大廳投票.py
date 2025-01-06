import discord
from discord.ext import commands
from discord.ui import Button, View
from collections import Counter
import json
from Bot import bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.reactions = True
intents.members = True

# 輔助函數
def load_player_data():
    """讀取玩家 JSON 資料"""
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_player_data(data):
    """儲存玩家 JSON 資料"""
    with open('player.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 按鈕投票邏輯
class VotingSession:
    def __init__(self, ctx, players):
        self.ctx = ctx
        self.players = players
        self.votes = {}
        self.round = 1
        self.candidates = [player_id for player_id, info in players.items() if info["狀態"] == "存活"]

    async def start_voting(self):
        """開始一輪投票"""
        channel = discord.utils.get(self.ctx.guild.text_channels, name="大廳")
        if not channel:
            channel = await self.ctx.guild.create_text_channel("大廳")

        view = View()
        for candidate_id in self.candidates:
            player = self.players[candidate_id]
            button = Button(label=f"{player['name']} ({player['序位']})", custom_id=str(candidate_id))
            button.callback = self.create_vote_callback(candidate_id)
            view.add_item(button)

        await channel.send(f"第 {self.round} 輪投票開始！請選擇你要投票的目標：", view=view)

    def create_vote_callback(self, candidate_id):
        """生成投票按鈕的回調函數"""
        async def vote_callback(interaction: discord.Interaction):
            voter_id = str(interaction.user.id)

            # 檢查投票者是否存在於玩家名單中
            if voter_id not in self.players:
                await interaction.response.send_message("你不在遊戲中，無法投票！", ephemeral=True)
                return

            # 檢查投票者是否存活
            if self.players[voter_id]["狀態"] != "存活":
                await interaction.response.send_message("你已死亡，無法參與投票！", ephemeral=True)
                return

            # 檢查是否已投過票
            if voter_id in self.votes:
                await interaction.response.send_message("你已經投過票了！", ephemeral=True)
                return

            # 記錄投票
            self.votes[voter_id] = candidate_id
            await interaction.response.send_message(f"你已投票給 {self.players[candidate_id]['name']}！", ephemeral=True)

            # 檢查是否所有存活玩家都已投票
            alive_players = [p for p in self.players.values() if p["狀態"] == "存活"]
            if len(self.votes) == len(alive_players):
                await self.end_voting()

        return vote_callback


    async def end_voting(self):
        """結束投票並計算結果"""
        vote_counts = Counter(self.votes.values())
        max_votes = max(vote_counts.values())
        potential_victims = [player_id for player_id, votes in vote_counts.items() if votes == max_votes]

        if len(potential_victims) == 1:
            # 單一最高票，改變其狀態為死亡
            victim_id = potential_victims[0]
            self.players[victim_id]["狀態"] = "死亡"
            save_player_data(self.players)
            channel = discord.utils.get(self.ctx.guild.text_channels, name="大廳")
            await channel.send(f"{self.players[victim_id]['name']} 獲得最高票，已死亡！")
        else:
            # 平票，進行下一輪投票
            if self.round == 2:
                # 第二輪仍平票，無人死亡
                channel = discord.utils.get(self.ctx.guild.text_channels, name="大廳")
                await channel.send("第二輪投票平票，無人死亡！")
            else:
                # 下一輪投票
                self.round += 1
                self.candidates = potential_victims
                self.votes = {}
                await self.start_voting()

# 指令處理
@bot.command()
async def 大廳投票(ctx):
    """在大廳進行按鈕投票"""
    players = load_player_data()
    if not any(p["狀態"] == "存活" for p in players.values()):
        await ctx.send("沒有存活的玩家，無法進行投票。")
        return

    voting_session = VotingSession(ctx, players)
    await voting_session.start_voting()