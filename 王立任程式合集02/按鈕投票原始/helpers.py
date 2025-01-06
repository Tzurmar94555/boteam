import json

def load_player_data():
    """讀取玩家 JSON 資料"""
    with open('player.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_player_data(data):
    """儲存玩家 JSON 資料"""
    with open('player.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def create_role_channel(guild, role):
    """創建角色專屬文字頻道"""
    channel_name = f"{role}投票區"
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    if existing_channel:
        return existing_channel

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
    }

    players = load_player_data()
    for player_id, info in players.items():
        if info["職業"] == role and info["狀態"] == "存活":
            member = guild.get_member(int(player_id))
            if member:
                overwrites[member] = discord.PermissionOverwrite(read_messages=True)

    return await guild.create_text_channel(channel_name, overwrites=overwrites)
