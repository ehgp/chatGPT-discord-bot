FROM python:3.8-alpine

COPY ./ /DiscordBot
WORKDIR /DiscordBot

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
