"""Main."""
from src import discord_bot
from src import telegram_bot
import sys
from chat_logs import chat

def check_verion() -> None:
    """Check Version."""
    import pkg_resources
    from src import log

    # init loggger
    logger = log.setup_logger(__name__)

    # Read the requirements.txt file and add each line to a list
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    # For each library listed in requirements.txt, check if the corresponding version is installed
    for package in required:
        # Use the pkg_resources library to get information about the installed version of the library
        package_name, package_verion = package.split('==')
        installed = pkg_resources.get_distribution(package_name)
        # Extract the library name and version number
        name, version = installed.project_name, installed.version
        # Compare the version number to see if it matches the one in requirements.txt
        if package != f'{name}=={version}':
            logger.info(f'{name} version {version} is installed but does not match the requirements')
            sys.exit()


if __name__ == '__main__':
    # check_verion()
    # discord_bot.run_discord_bot()
    chat.run_telegram_chat()
    # telegram_bot.run_telegram_bot()
