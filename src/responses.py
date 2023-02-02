from revChatGPT.Official import Chatbot
from asgiref.sync import sync_to_async
import os

chatbot = Chatbot(api_key=os.environ["OPENAI_TOKEN"])

async def handle_response(message) -> str:
    response = await sync_to_async(chatbot.ask)(message)
    responseMessage = response["choices"][0]["text"]

    return responseMessage
