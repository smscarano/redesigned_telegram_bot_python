from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import webbrowser
import pyautogui
from dotenv import load_dotenv
import os
import subprocess
import socket
import time
from monitorcontrol import get_monitors
    
def get_host_ip():
    try:
        # Get the host name of the machine
        host_name = socket.gethostname()

        # Get the IP address associated with the host name
        ip_address = socket.gethostbyname(host_name)

        return ip_address

    except socket.error as e:
        print(f"Error: {e}")
        return None
    
def is_number_between_1_and_9(value):
    try:
        num = int(value)
        # Check if the number is between 1 and 9 (inclusive)
        return 1 <= num <= 9
    except ValueError:
        # If the conversion to an integer fails, it's not a number
        return False

async def sendListHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global handlers
    for comando, manejador in handlers.items():
        full_command = '/' + comando
        await update.message.reply_text(full_command)

async def urlHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parts = update.message.text.split()
    if( len(parts) < 2 ):
        await update.message.reply_text("too short array ")
        return False
    url = parts[1]
    url_length = len(url)
    if( url_length < 12 ):
        await update.message.reply_text("too short url " + str(url_length))
        return False
    time.sleep(2)
    webbrowser.open(url)

async def setContrastHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parts = update.message.text.split()
    if( len(parts) < 2 ):
        await update.message.reply_text("too short array ")
        return False
    contrast = int(parts[1])
    for monitor in get_monitors():
        with monitor:
            monitor.set_contrast(contrast)

async def setLuminanceHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parts = update.message.text.split()
    if( len(parts) < 2 ):
        await update.message.reply_text("too short array ")
        return False
    luminance = int(parts[1])
    for monitor in get_monitors():
        with monitor:
            monitor.set_luminance(luminance)

async def poweroffMonitorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for monitor in get_monitors():
        with monitor:
             monitor.set_power_mode(4)

async def poweronMonitorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for monitor in get_monitors():
        with monitor:
             monitor.set_power_mode(1)

 

async def volumeUpHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.press('up')

async def volumeDownHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.press('down')

async def rightHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.press('right')

async def lefttHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.press('left')

async def closeWindowHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.hotkey('ctrl', 'w')

async def previousHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.hotkey('shift', 'p')

async def nextHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.hotkey('shift', 'n')

async def pauseHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.press('space')

async def fullHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pyautogui.press('f')

async def sendKeyHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command_tmp = update.message.text.split()
    command = command_tmp[1]
    print("recieved command: " + str(command))
    tab_n = is_number_between_1_and_9(command)
    if(tab_n == True):
        pyautogui.hotkey('ctrl', str(command))
    else:
        pyautogui.typewrite(command)
        pyautogui.press('enter')

async def rebootHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        command = 'shutdown /r /f /t 0'
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        # Handle the case when the command returns a non-zero exit code
        print("Error:")
        print(e.stderr)

async def poweroffHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        command = 'shutdown /s /f /t 0'
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        # Handle the case when the command returns a non-zero exit code
        print("Error:")
        print(e.stderr)

async def ipHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        ip_address = str(get_host_ip())
        await update.message.reply_text(ip_address)
    except:
        print("Error:")


async def monitor_dataHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        for monitor in get_monitors():
            with monitor:
                contast = "contast: " + str(monitor.get_contrast())
                luminance = "luminance: " + str(monitor.get_luminance())
                power_mode = "power_mode: " + str(monitor.get_power_mode())
                await update.message.reply_text(contast)
                await update.message.reply_text(luminance)
                await update.message.reply_text(power_mode)
                
    except:
        print("Error:")

async def screenSizeHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        size = pyautogui.size()
        await update.message.reply_text( str(size[0]) + " " + str(size[1]) )
                
    except:
        print("Error:")


async def clickHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.click()
    except:
        print("Error:")

async def doubleClickHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.click(2 , interval=0.1)
    except:
        print("Error:")


#username = get_os_username()
print("telegram bot started")

#load sensitive data from .env 
#make sure not to push it to repo
load_dotenv()
  
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

app = ApplicationBuilder().token(telegram_token).build()

unsorted_handlers = {
    "close": closeWindowHandler,
    "down": volumeDownHandler,
    "full": fullHandler,
    "ip": ipHandler,
    "list": sendListHandler,
    "pause": pauseHandler,
    "poweroff": poweroffHandler,
    "reboot": rebootHandler,
    "up": volumeUpHandler,
    "url": urlHandler,
    "c" : sendKeyHandler,
    "right" : rightHandler,
    "left" : lefttHandler,
    "previous" : previousHandler,
    "next" : nextHandler,
    "monitor_data" : monitor_dataHandler,
    "contrast" : setContrastHandler,
    "luminance" : setLuminanceHandler,
    "poweroffMonitor" : poweroffMonitorHandler,
    "poweronMonitorHandler" : poweronMonitorHandler,
    "size": screenSizeHandler,
    "click" : clickHandler,
    "doubleClick" : doubleClickHandler
}

handlers = dict(sorted(unsorted_handlers.items(), key=lambda item: item[0]))

#add command handlers
for comando, manejador in handlers.items():
    app.add_handler(CommandHandler(comando, manejador))

app.run_polling()
