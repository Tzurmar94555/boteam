import asyncio
import os
import re
import json
import threading
from dotenv import load_dotenv
from 爬蟲.reptile import test1
import discord
import yt_dlp
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from downloader import download_youtube_as_mp3
from check_in_json import check_in_json
from YT網址轉標題 import get_video_title
from songlink.reptile import test2  # 確保正確導入 test2 函數

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    voice_clients = {}
    yt_dl_options = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": "music/%(title)s.%(ext)s",
        "noplaylist": True,
    }
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {'options': '-vn'}
    loop_flags = {}
    play_queue = {}
    paused_flags = {}

    @client.event
    async def on_ready():
        print(f'{client.user} is now jaming')

    @client.event
    async def on_message(message):
        try:
            if message.content.startswith("!"):
                command = message.content.split()[0][1:]  # 取得命令
                input_value = " ".join(message.content.split()[1:])  # 取得命令參數
                print(command, input_value)
                
                if command == "play":
                    guild_id = message.guild.id
                    voice_client = None

                    # 檢查是否已經在語音頻道中
                    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
                        # 嘗試連接到語音頻道
                        try:
                            voice_client = await message.author.voice.channel.connect()
                            voice_clients[guild_id] = voice_client
                        except Exception as e:
                            await message.channel.send(f"無法連接語音頻道: {e}")
                            return
                    else:
                        voice_client = voice_clients[guild_id]

                    file_path = ""

                    if "https://" in input_value:
                        if check_in_json(input_value, "download_history.json"):
                            file_path = f"music/{get_video_title(input_value)}.mp3"
                        else:
                            try:
                                file_path = f"music/{download_youtube_as_mp3(input_value)}.mp3"
                            except Exception as e:
                                await message.channel.send(f"下載時發生錯誤: {e}")
                                return
                    else:
                        await message.channel.send(f"請輸入正確網址")
                        return

                    print(file_path)

                    if not os.path.exists(file_path):
                        await message.channel.send(f"找不到檔案：{file_path}")
                        return

                    try:
                        # 停止當前播放並播放新的音頻
                        if voice_client.is_playing():
                            voice_client.stop()

                        audio_source = FFmpegPCMAudio(file_path)
                        voice_client.play(audio_source, after=lambda e: on_song_end(guild_id) if e else None)
                        await message.channel.send(f"正在播放：{file_path}")

                    except Exception as e:
                        await message.channel.send(f"播放時發生錯誤: {e}")

                elif command == "loop":
                    guild_id = message.guild.id
                    if "https://" in input_value:
                        if check_in_json(input_value, "download_history.json"):
                            file_path = f"music/{get_video_title(input_value)}.mp3"
                        else:
                            try:
                                file_path = f"music/{download_youtube_as_mp3(input_value)}.mp3"
                            except Exception as e:
                                await message.channel.send(f"下載時發生錯誤: {e}")
                                return
                    else:
                        await message.channel.send(f"請輸入正確網址")
                        return

                    if not os.path.exists(file_path):
                        await message.channel.send(f"找不到檔案：{file_path}")
                        return

                    loop_flags[guild_id] = file_path
                    await message.channel.send(f"已啟用循環播放：{file_path}")

                    try:
                        if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
                            # 嘗試連接到語音頻道
                            try:
                                voice_client = await message.author.voice.channel.connect()
                                voice_clients[guild_id] = voice_client
                            except Exception as e:
                                await message.channel.send(f"無法連接語音頻道: {e}")
                                return
                        else:
                            voice_client = voice_clients[guild_id]

                        if voice_client.is_playing():
                            voice_client.stop()

                        await play_song(guild_id, file_path)

                    except Exception as e:
                        await message.channel.send(f"播放時發生錯誤: {e}")

                elif command == "stop":
                    try:
                        guild_id = message.guild.id
                        voice_client = voice_clients[guild_id]
                        if voice_client.is_playing():
                            voice_client.pause()
                            paused_flags[guild_id] = True
                            await message.channel.send("播放已暫停")
                        else:
                            await message.channel.send("目前沒有正在播放的音樂")
                    except Exception as e:
                        await message.channel.send(f"暫停播放時發生錯誤: {e}")
                elif command == "continue":
                    try:
                        guild_id = message.guild.id
                        voice_client = voice_clients[guild_id]
                        if paused_flags.get(guild_id, False):
                            voice_client.resume()
                            paused_flags[guild_id] = False
                            await message.channel.send("繼續播放")
                        else:
                            await message.channel.send("目前沒有暫停的音樂")
                    except Exception as e:
                        await message.channel.send(f"繼續播放時發生錯誤: {e}")
                elif command == "skip":
                    try:
                        guild_id = message.guild.id
                        voice_client = voice_clients[guild_id]
                        voice_client.stop()
                        await play_next_song(guild_id)
                        await message.channel.send("已跳過當前歌曲")
                    except Exception as e:
                        await message.channel.send(f"跳過歌曲時發生錯誤: {e}")
                elif command == "leave":
                    try:
                        guild_id = message.guild.id
                        await voice_clients[guild_id].disconnect()
                        del voice_clients[guild_id]
                        loop_flags.pop(guild_id, None)
                    except Exception as e:
                        print(e)
                elif command == "hello":
                    await message.channel.send("Hello!")
                elif command == "hotsong":
                    await message.channel.send(test1())
                elif command == "hotlink":
                    def run_test2():
                        youtube_urls = test2()
                        response = "\n".join(youtube_urls)
                        asyncio.run_coroutine_threadsafe(message.channel.send(f"KKBOX 每小時排行榜中的前 5 首歌曲的 YouTube 影片網址：\n{response}"), client.loop).result()

                    threading.Thread(target=run_test2).start()
                elif command == "add":
                    if "https://" in input_value:
                        if check_in_json(input_value, "download_history.json"):
                            video_title = get_video_title(input_value)  # 確保 video_title 被賦值
                            file_path = f"music/{video_title}.mp3"
                        else:
                            try:
                                video_title = download_youtube_as_mp3(input_value)
                                file_path = f"music/{video_title}.mp3"
                                await message.channel.send(f"下載完成：{file_path}")
                            except Exception as e:
                                await message.channel.send(f"下載時發生錯誤: {e}")
                                return
                        # 將歌曲資訊存至 add_song.json
                        song_info = {
                            "title": video_title,
                            "url": input_value
                        }
                        try:
                            with open("add_song.json", "r", encoding="utf-8") as f:
                                add_song_data = json.load(f)
                            add_song_data.append(song_info)
                            with open("add_song.json", "w", encoding="utf-8") as f:
                                json.dump(add_song_data, f, ensure_ascii=False, indent=4)
                            await message.channel.send(f"歌曲已新增至歌單：{video_title}")
                        except Exception as e:
                            await message.channel.send(f"儲存歌曲資訊時發生錯誤: {e}")
                elif command == "del":
                    song_title_to_delete = input_value.strip()
                    try:
                        with open("add_song.json", "r", encoding="utf-8") as f:
                            add_song_data = json.load(f)
                        
                        # 找到並刪除指定的歌曲
                        add_song_data = [song for song in add_song_data if song["title"] != song_title_to_delete]
                        
                        with open("add_song.json", "w", encoding="utf-8") as f:
                            json.dump(add_song_data, f, ensure_ascii=False, indent=4)
                        
                        await message.channel.send(f"歌曲已從歌單中刪除：{song_title_to_delete}")
                    except Exception as e:
                        await message.channel.send(f"刪除歌曲時發生錯誤: {e}")
                elif command == "list":
                    try:
                        if os.path.exists("add_song.json"):
                            with open("add_song.json", "r", encoding="utf-8") as f:
                                add_song_data = json.load(f)
                            song_titles = [song["title"] for song in add_song_data]
                            response = "\n".join(song_titles)
                            await message.channel.send(f"歌曲列表：\n{response}")
                        else:
                            await message.channel.send("沒有找到歌曲列表")
                    except Exception as e:
                        await message.channel.send(f"讀取歌曲列表時發生錯誤: {e}")
                elif command == "playlist":
                    guild_id = message.guild.id
                    try:
                        if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
                            # 嘗試連接到語音頻道
                            try:
                                voice_client = await message.author.voice.channel.connect()
                                voice_clients[guild_id] = voice_client
                            except Exception as e:
                                await message.channel.send(f"無法連接語音頻道: {e}")
                                return
                        else:
                            voice_client = voice_clients[guild_id]
                        await play_playlist(voice_client, message.channel)

                        with open("add_song.json", "r", encoding="utf-8") as f:
                            download_history = json.load(f)
                        play_queue[guild_id] = [f"music/{entry['title']}.mp3" for entry in download_history]
                        await message.channel.send("開始播放歌單中的所有歌曲")
                        await play_next_song(guild_id)
                    except Exception as e:
                        await message.channel.send(f"讀取時發生錯誤: {e}")
                elif command == "help":
                    try:
                        with open("help.json", "r", encoding="utf-8") as f:
                            help_data = json.load(f)
                        response = "\n".join([f"{cmd['command']}: {cmd['description']}" for cmd in help_data["commands"]])
                        await message.channel.send(f"指令列表：\n{response}")
                    except Exception as e:
                        await message.channel.send(f"讀取指令列表時發生錯誤: {e}")
                elif command == "playhs":
                    guild_id = message.guild.id
                    voice_client = None
                
                    # 檢查是否已經在語音頻道中
                    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
                        # 嘗試連接到語音頻道
                        try:
                            voice_client = await message.author.voice.channel.connect()
                            voice_clients[guild_id] = voice_client
                        except Exception as e:
                            await message.channel.send(f"無法連接語音頻道: {e}")
                            return
                    else:
                        voice_client = voice_clients[guild_id]

                    try:
                        youtube_urls = test2()
                        for url in youtube_urls:
                            if check_in_json(url, "download_history.json"):
                                file_path = f"music/{get_video_title(url)}.mp3"
                            else:
                                try:
                                    file_path = f"music/{download_youtube_as_mp3(url)}.mp3"
                                except Exception as e:
                                    await message.channel.send(f"下載時發生錯誤: {e}")
                                    continue
                
                            if not os.path.exists(file_path):
                                await message.channel.send(f"找不到檔案：{file_path}")
                                continue
                
                            try:
                                # 停止當前播放並播放新的音頻
                                if voice_client.is_playing():
                                    voice_client.stop()
                
                                audio_source = FFmpegPCMAudio(file_path)
                                voice_client.play(audio_source, after=lambda e: on_song_end(guild_id) if e else None)
                                await message.channel.send(f"正在播放：{file_path}")
                
                                # 等待當前歌曲播放完成
                                while voice_client.is_playing():
                                    await asyncio.sleep(1)
                
                            except Exception as e:
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
        voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(on_song_end(guild_id), client.loop))
        await client.get_channel(voice_client.channel.id).send(f"正在播放：{file_path}")

    async def play_playlist(voice_client, message_channel):
        try:
            with open("add_song.json", "r", encoding="utf-8") as f:
                add_song_data = json.load(f)

            for song in add_song_data:
                file_path = f"music/{song['title']}.mp3"
                voice_client.play(discord.FFmpegPCMAudio(file_path))
                await message_channel.send(f"正在播放：{song['title']}")
                while voice_client.is_playing():
                    await asyncio.sleep(1)
        except Exception as e:
            await message_channel.send(f"播放清單時發生錯誤: {e}")

    client.run(TOKEN)