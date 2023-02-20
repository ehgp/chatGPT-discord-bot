"""Main."""
import sys

from src import chat_log_model_tel_bot, discord_bot, log, telegram_bot

logger = log.setup_logger(__name__)

if __name__ == "__main__":
    # check_verion()
    # discord_bot.run_discord_bot()
    chat_log_model_tel_bot.run_telegram_chat()
    # telegram_bot.run_telegram_bot()
