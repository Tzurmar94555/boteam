import discord
from discord.ext import commands
from utils.azure_client import AzureClient
from utils.file_utils import save_image

class ImageGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.azure_client = AzureClient()  # 初始化 Azure 客户端

    @commands.Cog.listener()
    async def on_message(self, message):
        # 防止 bot 对自己的消息做出反应
        if message.author == self.bot.user:
            return

        # 如果消息是文本
        if message.content:
            prompt = message.content  # 获取用户的文本内容

            # 调用生成图像的函数
            generated_image_path = self.azure_client.generate_image(prompt)

            # 发送生成的图像到 Discord
            with open(generated_image_path, 'rb') as image_file:
                await message.channel.send(
                    content="Here is the image generated from your text:",
                    file=discord.File(image_file, filename="generated_image.png")
                )

def setup(bot):
    bot.add_cog(ImageGenerator(bot))
