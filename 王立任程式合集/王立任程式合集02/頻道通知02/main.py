from bot_setup import bot
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Set logging level
    bot.run("你的金鑰")  # Add your bot token
