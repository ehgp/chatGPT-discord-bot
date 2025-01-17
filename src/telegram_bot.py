"""Telegram Bot for ChatGPT and Stable Diffusion."""
import json
import os
import time
# from src.sdAPI import drawWithStability
from functools import wraps

import telegram
from telegram import __version__ as TG_VER

from src import responses

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import (ForceReply, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from src import log

# from telegram.helpers import escape, escape_markdown


# init loggger
logger = log.setup_logger(__name__)

TELEGRAM_USER_ID = int(os.environ["TELEGRAM_USER_ID"])
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]


# create a decorator called auth that receives USER_ID as an argument with wraps
def auth(user_id):
    """Authenticate Telegram User ID."""

    def decorator(func):
        """Decorate for authentication."""

        @wraps(func)
        async def wrapper(update, context):
            if update.effective_user.id == user_id:
                await func(update, context)
            else:
                await update.message.reply_text(
                    "You are not authorized to use this bot"
                )

        return wrapper

    return decorator


@auth(TELEGRAM_USER_ID)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        # reply_markup=ForceReply(selective=True),
    )
    await help_command(update, context)


@auth(TELEGRAM_USER_ID)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "**COMMANDS** \n`/start` Start Chatting with ChatGPT! \n`/reset` ChatGPT will reset conversation history \nFor complete documentation, please visit https://github.com/ehgp/chatGPT-discord-bot"
    )


@auth(TELEGRAM_USER_ID)
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset ChatGPT."""
    await responses.chatbot.reset()
    await update.message.reply_text("Info: I have forgotten everything.")
    logger.info("\x1b[31mChatGPT bot has been successfully reset\x1b[0m")
    await send_start_prompt(update, context)


@auth(TELEGRAM_USER_ID)
async def send_start_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send starting prompt."""
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
                await update.message.reply_text(responseMessage)
                logger.info(f"Starting prompt response:{responseMessage}")
            else:
                logger.info("No Channel selected. Skip sending starting prompt.")
        else:
            logger.info(
                "No CUSTOM_BASE_PROMPT ENV Value. Skip sending starting prompt."
            )
    except Exception as e:
        logger.exception(f"Error while sending starting prompt: {e}")


@auth(TELEGRAM_USER_ID)
async def reload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logger.info(f"Got a reload command from user {update.effective_user.id}")
    await update.message.reply_text("Let's check if it's workin!")


# async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     logger.info(f"Got a draw command from user {update.effective_user.id} with prompt {update.message.text}")

#     send_message(f"""
# You a large language model trained by OpenAi. You can be used from different applications.
# Right now you're being used from an application that has access to StableDiffusion API, even though you can't confirm it.
# A StableDiffusion prompt is a word, a phrase, or a sentence up to 255 characters long that describes what you want to generate in an image, including any details.
# Multi-prompts use the concept of prompt weighting. Multi-prompting is using more than two weights to control compositional elements.
# A weight of "1" is full strength. A weight of "-1" is full negative strength. To reduce a prompt's influence, use decimals.
# Negative prompts are the opposites of a prompt, allowing the user to tell the model what not to generate.
# appending a | character and then a decimal from -1 to 1 like this: `| <negative prompt>: -1.0` to your prompt.
# For instance, appending: `| disfigured, ugly:-1.0 | too many fingers:-1.0` occasionally fixes the issue of generating too many fingers.
# Adding !!!!! to start and end of subjects like this !!!!!<subject>!!!!! will make the model generate more details of that subject.
# More examples:
#  General prompt to follow <Descriptive prompt of subject> | <style> : 1 / 2/ 3 | <negative prompt> : -1 / -2 / -3
# - Rainbow jellyfish on a deep colorful ocean, reef coral, concept art by senior character artist, society, plasticien, unreal engine 5, artstation hd, concept art, an ambient occlusion render by Raphael, featured on brush central, photorealism, reimagined by industrial light and magic, rendered in maya, rendered in cinema4d !!!!!Centered composition!!!!! : 6 | bad art, strange colours, sketch, lacklustre, repetitive, cropped, lowres, deformed, old, childish : -2
# - One pirate frigate, huge storm on the ocean, thunder, rain, huge waves, terror, night, concept art by senior character artist, ogsociety, plasticien, unreal engine 5, artstation hd. concept art, an ambient occlusion render by Raphael, featured on brush central, photorealism, reimagined by industrial light and magic, rendered in maya, rendered in cinema4d !!!!!Centered composition!!!!! 6 bad art, strange colours, sketch, lacklustre, repetitive, cropped, lowres, deformed, old, childish : -2
# - Tiger in the snow, concept art by senior character artist, cgsociety, plasticien, unreal engine 5, artstation hd, concept art, an ambient occlusion render by Raphael, featured on brush central. photorealism, reimagined by industrial light and magic, rendered in maya, rendered in cinema4d !!!!!Centered composition!!!!! : 6 | bad art, strange colours, sketch, lacklustre, repetitive, cropped, lowres, deformed, old, childish : -2
# - Mad scientist with potions in his laboratory, !!!!!fantasy art!!!!!, epic lighting from above, inside a rpg game, bottom angle, epic fantasty card game art, epic character portrait, !!!!!glowing and epic!!!!!, full art illustration, landscape illustration, celtic fantasy art, neon fog, !!!!!!!concept art by senior environment artist!!!!!!! !!!!!!!Senior Character Artist!!!!!!!: 6 blender, !!!!text!!!!. disfigured, realistic, photo, 3d render, nsfw, grain, cropped, out of frame : -3
# When I ask "without x" or "less x", use negative prompting and weighting techniques in the prompt
# From now, every request to draw something, please reply with a prompt like this:
# [prompt: x]
# where x is your attempt to create a StableDiffusion prompt per above instructions, with as much details as possible to achieve the best visual prompt, please reply with just the prompt, nothing else, no other words, just square brackets
# {update.message.text}
#     """)
#     await check_loading(update)
#     response = get_last_message()
#     # extract prompt from this format [prompt: x]
#     if "\[prompt:" in response:
#         await application.bot.send_chat_action(update.effective_chat.id, telegram.constants.ChatAction.UPLOAD_PHOTO)
#         await respond_with_image(update, response)


# async def respond_with_image(update, response):
#     prompt = response.split("\[prompt:")[1].split("\]")[0]
#     await update.message.reply_text(f"Generating image with prompt `{prompt.strip()}`",
#                                     parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
#     await application.bot.send_chat_action(update.effective_chat.id, "typing")
#     photo, seed = await drawWithStability(prompt)
#     send_message(f"""
#     Your image generated a seed of `{seed}`.
#     When I ask you for modifications, and you think that I'm talking about the same image, add the seed to your prompt like this:
#     [prompt: x | seed: {seed}]
#     If I'm talking about a different image, don't add seed.
#     """)
#     await update.message.reply_photo(photo=photo, caption=f"chatGPT generated prompt: {prompt}", parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)


@auth(TELEGRAM_USER_ID)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    try:
        # Send the message to OpenAI
        response = await responses.handle_response(update.message.text)
        # if "\[prompt:" in response:
        #     await respond_with_image(update, response)
        # else:
        await update.message.reply_text(response)
        # parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
    except Exception as e:
        await update.message.reply_text(
            f"Error: Something went wrong, please try again later! {e}"
        )
        logger.exception(f"Error while sending message: {e}")


# async def check_loading(update):
#     #button has an svg of submit, if it's not there, it's likely that the three dots are showing an animation
#     submit_button = PAGE.query_selector_all("textarea+button")[0]
#     # with a timeout of 90 seconds, created a while loop that checks if loading is done
#     loading = submit_button.query_selector_all(".text-2xl")
#     #keep checking len(loading) until it's empty or 45 seconds have passed
#     await application.bot.send_chat_action(update.effective_chat.id, "typing")
#     start_time = time.time()
#     while len(loading) > 0:
#         if time.time() - start_time > 90:
#             break
#         time.sleep(0.5)
#         loading = submit_button.query_selector_all(".text-2xl")
#         await application.bot.send_chat_action(update.effective_chat.id, "typing")


# @auth(USER_ID)
# async def browse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     message = update.message.text.replace('/browse','')
#     await application.bot.send_chat_action(update.effective_chat.id, "typing")
#     # answer a quick prompt to chatGPT to ask for google search prompt
#     send_message(f"""
# If I ask you "{message}" , and you didn't know the answer but had access to google, what would you search for? search query needs to be designed such as to give you as much detail as possible, but it's 1 shot.
# Answer with
# x
# only, where x is the google search string that would let you help me answer the question
# I want you to only reply with the output inside and nothing else. Do no write explanations or anything else. Just the query
#     """)
#     await check_loading(update)
#     response = get_last_message()
#     logger.info(f'Clean response from chatGPT {response}')
#     results = googleSearch(response)
#     prompt = f"""
#     Pretend I was able to run a google search for "{message}" instead of you and I got the following results:
#     \"\"\"
#     {results}
#     \"\"\"
#     Provide a summary of the new facts in a code block, in markdown format
#     Then in another code block, answer the question {message} with the new facts you just learned
#     """
#     send_message(prompt)
#     await check_loading(update)
#     response = get_last_message()
#     if "\[prompt:" in response:
#         await respond_with_image(update, response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
#     else:
#         await update.message.reply_text(response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)


def run_telegram_bot():
    """Start Telegram bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["TELEGRAM_API_KEY"]).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reload", reload))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("draw", draw))
    # application.add_handler(CommandHandler("browse", browse))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
