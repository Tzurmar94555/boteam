import discord
from discord.ext import commands
from discord.ui import Button, View
import json
from Bot import bot

# 輔助函數
def load_player_data():
    """讀取玩家 JSON 資料"""
    # 讀取 player.json 檔案，並將內容解析為 Python 字典返回
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_player_data(data):
    """儲存玩家 JSON 資料"""
    # 將玩家資料寫回到 player.json 檔案，保持 UTF-8 編碼並格式化 JSON
    with open('player.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def create_role_channel(guild, role):
    """創建角色專屬文字頻道"""
    channel_name = f"{role}投票區"  # 頻道名稱為角色名稱+投票區
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    
    # 如果該頻道已經存在，則返回該頻道
    if existing_channel:
        return existing_channel

    # 設定頻道權限，預設角色無法讀取消息
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
    }

    # 讀取玩家資料
    players = load_player_data()
    for player_id, info in players.items():
        # 如果玩家職業是指定角色，且玩家狀態為存活，則該玩家可以讀取該頻道
        if info["職業"] == role and info["狀態"] == "存活":
            member = guild.get_member(int(player_id))
            if member:
                overwrites[member] = discord.PermissionOverwrite(read_messages=True)

    # 創建新頻道並設置權限
    return await guild.create_text_channel(channel_name, overwrites=overwrites)

# 按鈕處理器
class VoteButton(Button):
    def __init__(self, label, custom_id, callback):
        # 初始化按鈕，設置顯示文本、custom_id 和回調函數
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        # 按下按鈕後執行的回調函數
        await self.callback_function(interaction)

class VotingSession:
    def __init__(self, ctx, role):
        self.ctx = ctx  # 當前的 Discord 上下文（包括伺服器、頻道等）
        self.role = role  # 角色，例如 "預言家", "守衛", "狼人"
        self.players = load_player_data()  # 讀取玩家資料
        self.votes = {}  # 用來紀錄玩家投票結果的字典

    async def start_voting(self):
        """開始投票流程"""
        guild = self.ctx.guild  # 獲取伺服器信息
        channel = await create_role_channel(guild, self.role)  # 創建角色專屬頻道
        view = View()  # 創建一個新的視圖（包含按鈕）

        # 為每個存活的玩家創建投票按鈕
        for player_id, info in self.players.items():
            if info["狀態"] == "存活":
                # 為每個存活的玩家創建一個投票按鈕
                button = VoteButton(label=f"{info['name']} ({info['序位']})", 
                                    custom_id=str(player_id), 
                                    callback=self.handle_vote)
                view.add_item(button)

        # 在角色專屬頻道中發送投票開始消息並顯示按鈕
        await channel.send(f"{self.role}請進行投票！", view=view)

    async def handle_vote(self, interaction):
        """處理投票邏輯"""
        voter_id = str(interaction.user.id)  # 投票者的 ID
        if voter_id not in self.players:
            # 如果投票者不在玩家列表中，返回錯誤消息
            await interaction.response.send_message("你不在投票名單中！", ephemeral=True)
            return

        # 檢查該玩家是否已經投過票
        if voter_id in self.votes:
            await interaction.response.send_message("你已經投過票了！", ephemeral=True)
            return

        # 紀錄投票結果
        target_id = interaction.data['custom_id']  # 投票對象的 ID
        self.votes[voter_id] = target_id  # 將投票結果保存

        await interaction.response.send_message(f"你已投票給 {self.players[target_id]['name']}！", ephemeral=True)

        # 如果所有玩家都投票完成，結束投票
        if len(self.votes) == len([p for p in self.players.values() if p["狀態"] == "存活" and p["職業"] == self.role]):
            await self.end_voting()

    async def end_voting(self):
        """結束投票並處理結果"""
        # 投票結果處理邏輯
        if self.role == "預言家":
            # 如果角色是預言家，根據投票結果向每個投票者發送查驗結果
            for voter, target in self.votes.items():
                role = self.players[target]["職業"]
                result = "狼人" if role == "狼人" else "好人"
                user = await self.ctx.guild.fetch_member(int(voter))
                await user.send(f"你查驗的玩家是：{self.players[target]['name']}，結果為：{result}")

        elif self.role == "守衛":
            # 如果角色是守衛，將守衛的守護對象記錄下來
            for voter, target in self.votes.items():
                self.players[voter]["守護"] = target

        elif self.role == "狼人":
            # 如果角色是狼人，計算每個玩家獲得的票數，並將票數最多的玩家設為死亡
            vote_counts = {}
            for target in self.votes.values():
                vote_counts[target] = vote_counts.get(target, 0) + 1

            # 找到被票數最多的玩家
            victim = max(vote_counts, key=vote_counts.get)
            self.players[victim]["狀態"] = "死亡"

        # 儲存更新後的玩家資料
        save_player_data(self.players)
        # 在頻道中發送投票結束的消息
        await self.ctx.send(f"{self.role}投票結束！結果已紀錄。")

# 指令部分
@bot.command()
async def 投票(ctx, role):
    """開始指定角色的投票（白天/夜晚）"""
    # 創建並啟動投票會話
    session = VotingSession(ctx, role) 
    await session.start_voting()

