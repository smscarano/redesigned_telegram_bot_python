# redesigned_telegram_bot_python

## REQUIRED LIBRARIES
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
   Once the bot is running on your PC, chat with your bot using Telegram and send the command `/list`.  
   You should receive a message from the bot consisting of a list of available commands.  

## EXAMPLES
   `/list` you'll recieve a telegram message from the bot with a list of available commands.  
   `/url https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs` will open the provided url on your default web browser.  
   `/pause` pauses youtube emulating spacebar keypress, it can be used on programs that have the same hotkey.  
   `/close` closes active browser tab
   `/full` emulates pressing the 'f' key, which is the hotkey for YouTube and other software/sites fullscreen toggle.  
   `/up` emulates pressing the up key, which is the hotkey for increasing volume on YouTube and other software/sites.  
   `/down` opposite of `/up`.  
