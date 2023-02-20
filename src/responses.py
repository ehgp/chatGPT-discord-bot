"""Responses."""
import os

from asgiref.sync import sync_to_async
from revChatGPT.Official import Chatbot

from src import log

chatbot = Chatbot(api_key=os.environ["OPENAI_TOKEN"])

# init loggger
logger = log.setup_logger(__name__)


async def handle_response(message) -> str:
    """Handle Response from Chatbot."""
    response = await sync_to_async(chatbot.ask)(message)
    responseMessage = response["choices"][0]["text"]

    return responseMessage
