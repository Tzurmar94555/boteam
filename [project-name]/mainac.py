while voice_client.is_playing():
    await asyncio.sleep(1)

try:
    await message.channel.send(f"播放時發生錯誤: {e}")

except Exception as e:
    await message.channel.send(f"讀取歌曲列表時發生錯誤: {e}")
except Exception as e:
    print(f"處理訊息時發生錯誤: {e}")

async def play_next_song(guild_id):
    if play_queue.get(guild_id):
        file_path = play_queue[guild_id].pop(0)
        if os.path.exists(file_path):
            voice_client = voice_clients.get(guild_id)
            if voice_client is None:
                await client.get_channel(voice_client.channel.id).send(f"找不到語音客戶端")
                return
            audio_source = FFmpegPCMAudio(file_path)
            voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(guild_id), client.loop))
            await client.get_channel(voice_client.channel.id).send(f"正在播放：{file_path}")
        else:
            await client.get_channel(voice_client.channel.id).send(f"找不到檔案：{file_path}")
            await play_next_song(guild_id)

def on_song_end(guild_id):
    if guild_id in loop_flags:
        file_path = loop_flags[guild_id]
        asyncio.run_coroutine_threadsafe(play_song(guild_id, file_path), client.loop)

async def play_song(guild_id, file_path):
    voice_client = voice_clients.get(guild_id)
    if voice_client is None:
        await client.get_channel(voice_client.channel.id).send(f"找不到語音客戶端")
        return
    audio_source = FFmpegPCMAudio(file_path)
    voice_client.play(audio_source, after=lambda e: on_song_end(guild_id) if e else asyncio.run_coroutine_threadsafe(play_next_song(guild_id), client.loop))