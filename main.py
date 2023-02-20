"""Main."""
from src import discord_bot
from src import telegram_bot
from src import chat_log_model_tel_bot
from src import log
import sys

logger = log.setup_logger(__name__)

if __name__ == "__main__":
    # check_verion()
    # discord_bot.run_discord_bot()
    chat_log_model_tel_bot.run_telegram_chat()
    # telegram_bot.run_telegram_bot()
