import discord
from discord.ui import Button, View
from helpers import load_player_data, save_player_data, create_role_channel

class VoteButton(Button):
    def __init__(self, label, custom_id, callback):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        await self.callback_function(interaction)

class VotingSession:
    def __init__(self, ctx, role):
        self.ctx = ctx
        self.role = role  # e.g., "預言家", "守衛", "狼人"
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

        # 檢查該玩家是否已經投過票
        if voter_id in self.votes:
            await interaction.response.send_message("你已經投過票了！", ephemeral=True)
            return

        # 紀錄投票結果
        target_id = interaction.data['custom_id']
        self.votes[voter_id] = target_id

        await interaction.response.send_message(f"你已投票給 {self.players[target_id]['name']}！", ephemeral=True)

        # 如果所有玩家投票完成，結束投票
        if len(self.votes) == len([p for p in self.players.values() if p["狀態"] == "存活" and p["職業"] == self.role]):
            await self.end_voting()

    async def end_voting(self):
        """結束投票並處理結果"""
        # 投票結果處理邏輯
        if self.role == "預言家":
            for voter, target in self.votes.items():
                role = self.players[target]["職業"]
                result = "狼人" if role == "狼人" else "好人"
                user = await self.ctx.guild.fetch_member(int(voter))
                await user.send(f"你查驗的玩家是：{self.players[target]['name']}，結果為：{result}")

        elif self.role == "守衛":
            for voter, target in self.votes.items():
                self.players[voter]["守護"] = target

        elif self.role == "狼人":
            vote_counts = {}
            for target in self.votes.values():
                vote_counts[target] = vote_counts.get(target, 0) + 1

            # 找到被票數最多的玩家
            victim = max(vote_counts, key=vote_counts.get)
            self.players[victim]["狀態"] = "死亡"

        save_player_data(self.players)
        await self.ctx.send(f"{self.role}投票結束！結果已紀錄。")
