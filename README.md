# chatGPT-discord-bot

> ## This is a project that provides you to build your own Discord bot using ChatGPT
>
> ⭐️ If this repo helps you, a star is the biggest support for me and also helps you stay up-to-date
---
> **Warning**
>
> ### 2023-02-01 Update: Now using the official ChatGPT API

## Features

### Discord Bot

* `/chat [message]` Chat with ChatGPT!
* `/private` ChatGPT switch to private mode
* `/public`  ChatGPT switch to public  mode
* `/reset`   ChatGPT conversation history will be erased

### Telegram Bot

* `/start` Start up ChatGPT!
* `/reset`   ChatGPT conversation history will be erased

## Chat

![image](https://user-images.githubusercontent.com/89479282/206497774-47d960cd-1aeb-4fba-9af5-1f9d6ff41f00.gif)

## Mode

* `public mode (default)`  the bot directly reply on the channel

  ![image](https://user-images.githubusercontent.com/89479282/206565977-d7c5d405-fdb4-4202-bbdd-715b7c8e8415.gif)
* `private mode` the bot's reply can only be seen by who use the command

  ![image](https://user-images.githubusercontent.com/89479282/206565873-b181e600-e793-4a94-a978-47f806b986da.gif)

## Setup

### Install

1. `pip install -r requirements.txt`
2. **Change the file name of `.env.example` to `.env`**

### Step 1: Create a Discord bot

1. Go to <https://discord.com/developers/applications> create an application
2. Build a Discord bot under the application
3. Get the token from bot setting

   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. Store the token to `.env` under the `DISCORD_BOT_TOKEN`

   ![image](https://user-images.githubusercontent.com/89479282/207357762-94234aa7-aa55-4504-8dfd-9c68ae23a826.png)

5. Turn MESSAGE CONTENT INTENT `ON`

   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)

6. Invite your bot to your server via OAuth2 URL Generator

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)

   Enable `bot` and `applications.commands` scopes, copy the generated URL and paste it into your browser

### Step 2: Generate a OpenAI API key

1. Go to <https://beta.openai.com/account/api-keys>

2. Click Create new secret key

   ![image](https://user-images.githubusercontent.com/89479282/207970699-2e0cb671-8636-4e27-b1f3-b75d6db9b57e.PNG)

3. Store the SECRET KEY to `.env` under the `OPENAI_TOKEN`

### Step 3: Run the bot on the desktop

1. Open a terminal or command prompt
2. Navigate to the directory where you installed the ChatGPT Discord bot
3. Run `python3 main.py` to start the bot

### Step 3: Run the bot with docker

### Start the bot

1. Build the Dcoker image & Run the Docker container `docker compose up -d`
2. Inspect whether the bot works well `docker logs -t chatgpt-discord-bot`

OR

1. sh start.sh

#### Stop the bot

* `docker ps` to see the list of running services
* `docker stop <BOT CONTAINER ID>` to stop the running bot

OR

1. sh stop.sh

### Have A Good Chat

## Optional: Setup starting prompt

* A starting prompt would be invoked when the bot is first started or reset
* You can set it up by modifying the content in `.env.example.CUSTOM_BASE_PROMPT`
* All the text in the file will be fired as a prompt to the bot
* Get the first message from ChatGPT in your discord channel!

   1. Right-click the channel you want to recieve the message, `Copy  ID`

        ![channel-id](https://user-images.githubusercontent.com/89479282/207697217-e03357b3-3b3d-44d0-b880-163217ed4a49.PNG)

   2. paste it into `.env` under `DISCORD_CHANNEL_ID`

## FMP_API

<https://site.financialmodelingprep.com/>
