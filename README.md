# redesigned_telegram_bot_python

## CREATING A NEW TELEGRAM BOT
On telegram APP use the `/newbot` command to create a new bot. `@BotFather` will ask you for a name and username, then generate an authentication token for your new bot.  
The name of your bot is displayed in contact details and elsewhere.  
The username is a short name, used in search, mentions, and t.me links. Usernames are 5-32 characters long and not case-sensitive – but may only include Latin characters, numbers, and underscores. Your bot's username must end in 'bot’, like 'tetris_bot' or 'TetrisBot'.  
The token is a string, like `112224443:AAHdqTcvCH1vGWJxfSFAfSAs0K5PALDsaw`, which is required to authorize the bot and send requests to the Bot API. Keep your token secure and store it safely; it can be used by anyone to control your bot.  
Unlike the bot’s name, the username cannot be changed later – so choose it carefully.  
When sending a request to `api.telegram.org`, remember to prefix the word ‘bot’ to your token.  
[Source](https://core.telegram.org/bots/features "Link to telegram site")  

## INSTALL REQUIRED LIBRARIES
``pip install -r requirements.txt``

## CREATE .env FILE
Copy .envexample to .env and add your secret TELEGRAM TOKEN.
It should look like `TELEGRAM_BOT_TOKEN = 'yourtoken'`.
Replace the example string with your token.
Never push your token to your repository or share it.


## RUN SCRIPT
### On Windows:  
  * python main.py

### On Linux:  
  * python3 main.py 

## BOT USAGE
   Once the bot is running on your PC, chat with your bot using Telegram and send the command you want.  
   After sending `/list` you should receive a message from the bot consisting of a list of available commands.  

## EXAMPLES
   `/list` you'll recieve a telegram message from the bot with a list of available commands.  
   `/url https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs` will open the provided url on your default web browser.  
   `/pause` pauses youtube emulating spacebar keypress, it can be used on programs that have the same hotkey.  
   `/close` closes active browser tab
   `/full` emulates pressing the 'f' key, which is the hotkey for YouTube and other software/sites fullscreen toggle.  
   `/up` emulates pressing the up key, which is the hotkey for increasing volume on YouTube and other software/sites.  
   `/down` opposite of `/up`.  
