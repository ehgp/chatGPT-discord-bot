"""Discord Bot for ChatGPT."""
import os

import discord
from discord import option

from src import log, responses

logger = log.setup_logger(__name__)

isPrivate = False

# class aclient(discord.Client):
#     def __init__(self) -> None:
#         super().__init__(intents=discord.Intents.default())
#         self.tree = app_commands.CommandTree(self)
#         self.activity = discord.Activity(
#             type=discord.ActivityType.watching, name="/chat | /help"
#         )


async def send_message(message, user_message):
    await message.response.defer(ephemeral=isPrivate)
    try:
        response = "> **" + user_message + "** - <@" + str(message.user.id) + "> \n\n"
        response = f"{response}{await responses.handle_response(user_message)}"
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                await message.followup.send(parts[0])
                # Send the code block in a seperate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += (
                        line + "\n"
                    )  # Add the line and seperate with new line

                # Send the code block in a separate message
                if len(formatted_code_block) > 2000:
                    code_block_chunks = [
                        formatted_code_block[i : i + 1900]
                        for i in range(0, len(formatted_code_block), 1900)
                    ]
                    for chunk in code_block_chunks:
                        await message.followup.send("```" + chunk + "```")
                else:
                    await message.followup.send("```" + formatted_code_block + "```")

                # Send the remaining of the response in another message

                if len(parts) >= 3:
                    await message.followup.send(parts[2])
            else:
                response_chunks = [
                    response[i : i + 1900] for i in range(0, len(response), 1900)
                ]
                for chunk in response_chunks:
                    await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send(
            f"> **Error: Something went wrong, please try again later!** {e}"
        )
        logger.exception(f"Error while sending message: {e}")


async def send_start_prompt(client):
    import os
    import os.path

    try:
        if os.environ["CUSTOM_BASE_PROMPT"]:
            if os.environ["DISCORD_CHANNEL_ID"]:
                logger.info(
                    f"Send starting prompt with size {len(os.environ['CUSTOM_BASE_PROMPT'])}"
                )
                responseMessage = await responses.handle_response(
                    os.environ["CUSTOM_BASE_PROMPT"]
                )
                channel = client.get_channel(int(os.environ["DISCORD_CHANNEL_ID"]))
                await channel.send(responseMessage)
                logger.info(f"Starting prompt response:{responseMessage}")
            else:
                logger.info("No Channel selected. Skip sending starting prompt.")
        else:
            logger.info(
                "No CUSTOM_BASE_PROMPT ENV Value. Skip sending starting prompt."
            )
    except Exception as e:
        logger.exception(f"Error while sending starting prompt: {e}")


def run_discord_bot():
    # Note: This is not generally recommended by Discord. It is this way only for the two servers running this release.
    intents = discord.Intents.all()

    client = discord.Bot(intents=intents)

    @client.event
    async def on_ready():
        await send_start_prompt(client)
        await client.tree.sync()
        logger.info(f"{client.user} is now running!")

    @client.slash_command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
        await send_message(interaction, user_message)

    @client.slash_command(name="private", description="Toggle private access")
    async def private(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            logger.info("\x1b[31mSwitch to private mode\x1b[0m")
            await interaction.followup.send(
                "> **Info: Next, the response will be sent via private message. If you want to switch back to public mode, use `/public`**"
            )
        else:
            logger.info("You already on private mode!")
            await interaction.followup.send(
                "> **Warn: You already on private mode. If you want to switch to public mode, use `/public`**"
            )

    @client.slash_command(name="public", description="Toggle public access")
    async def public(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**"
            )
            logger.info("\x1b[31mSwitch to public mode\x1b[0m")
        else:
            await interaction.followup.send(
                "> **Warn: You already on public mode. If you want to switch to private mode, use `/private`**"
            )
            logger.info("You already on public mode!")

    @client.slash_command(
        name="reset", description="Complete reset ChatGPT conversation history"
    )
    async def reset(interaction: discord.Interaction):
        responses.chatbot.reset()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Info: I have forgotten everything.**")
        logger.info("\x1b[31mChatGPT bot has been successfully reset\x1b[0m")
        await send_start_prompt(client)

    @client.slash_command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(
            ":star:**COMMANDS** \n`/chat [message]` Chat with ChatGPT!\n`/public` ChatGPT switch to public mode \n`/private` ChatGPT switch to private mode \n`/reset` ChatGPT will reset conversation history \nFor complete documentation, please visit https://github.com/ehgp/chatGPT-discord-bot"
        )
        logger.info("\x1b[31mSomeone need help!\x1b[0m")

    TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    client.run(TOKEN)
