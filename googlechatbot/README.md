# Google Chat Bot

## Get Started

1. Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Add relevant scopes to the project.
3. Create a new service account and download the JSON key file.

## Scopes

1. GMAIL: ["https://www.googleapis.com/auth/gmail.send"]
2. CALENDAR: ["https://www.googleapis.com/auth/calendar"]
3. DRIVE: ["https://www.googleapis.com/auth/drive"]
4. SHEETS: ["https://www.googleapis.com/auth/spreadsheets"]
5. CHAT: ["https://www.googleapis.com/auth/chat.bot","https://www.googleapis.com/auth/chat.messages","https://www.googleapis.com/auth/chat.spaces"]

## User Auth

  ```python
  import os
  from pathlib import Path
  from google.auth.transport.requests import Request
  from google_auth_oauthlib.flow import InstalledAppFlow
  from google.oauth2.credentials import Credentials

  token_file = Path(os.path.join(os.getcwd(),"token.json"))
  cred_file = Path(os.path.join(os.getcwd(),"credentials.json"))
  SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
  if os.path.exists(token_file):
      creds = Credentials.from_authorized_user_file(token_file, SCOPES)
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
  else:
      flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
      creds = flow.run_local_server(port=0)
      with open(token_file, "w") as token:
          token.write(creds.to_json())
  ```

## Webhook

  ```python
  import requests
  import json
  url = ''
  bot_message = {
      'text' : 'Hello from Python! :tada:'
  }
  message_headers = {'Content-Type' : 'application/json; charset=UTF-8'}
  respose = requests.post(url, data=json.dumps(bot_message), headers=message_headers)
  print(response.status_code)
  ```

## Service Account Auth

### Normal Service Account

  ```python
  from oauth2client.service_account import ServiceAccountCredentials
  creds_sa = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', SCOPES)
  ```

### Domain Wide Delegation Developer Preview Service Account

  ```python
  from oauth2client.service_account import ServiceAccountCredentials
  url = 'https://chat.googleapis.com/$discovery/rest?version=v1&labels=DEVELOPER_PREVIEW&key={YOUR_API_KEY}'
  creds_sa = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', SCOPES)
  delegated_chat_creds = creds_sa.create_delegated('me@gmail.com')
  chat = build('chat', 'v1', credentials=delegated_chat_creds, discoveryServiceUrl=url)
  ```

## Stack

1. Flask with 2 api endpoints with scheduled processes
2. Docker
3. Google Cloud API

## Local Development

1. Get your client secret file from the Google Cloud Console.
2. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of your client secret file.
3. Run `python main.py` to start the server.
