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
import platform

def get_operating_system():
    try:
        system_name = platform.system()
        return system_name
    except Exception as e:
        print(f"Error getting operating system: {e}")
        return None

def get_username_linux():
    try:
        username = os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME')
        return username
    except Exception as e:
        print(f"Error getting username on Linux: {e}")
        return None

def get_username_windows():
    try:
        username = os.getenv('USERNAME')
        return username
    except Exception as e:
        print(f"Error getting username on Windows: {e}")
        return None
        
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = str(s.getsockname()[0])
        return ip_addr

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

def print_colored_text(text, color_name):
    try:
        color_codes = {
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37
        }

        # Check if the specified color is in the dictionary
        if color_name not in color_codes:
            raise ValueError(f"Invalid color: {color_name}")

        color_code = color_codes[color_name]

        # Print colored text using ANSI escape codes
        print(f"\033[{color_code}m{text}\033[0m")
    except:
        print("error calling print_colored_text()")

async def sendListHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global handlers
    try:
        command_list = '\n'.join([f'/{comando}' for comando, _ in handlers.items()])
        await update.message.reply_text(command_list)
    except Exception as e:
        print(f"Error in sendListHandler: {e}")

async def urlHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        parts = update.message.text.split()
        if len(parts) < 2:
            await update.message.reply_text("too short array ")
            return False
        url = parts[1]
        url_length = len(url)
        if url_length < 12:
            await update.message.reply_text("too short url " + str(url_length))
            return False
        time.sleep(2)
        webbrowser.open(url)
    except Exception as e:
        await update.message.reply_text(f"Error in urlHandler: {e}")

async def setContrastHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        parts = update.message.text.split()
        if len(parts) < 2:
            await update.message.reply_text("too short array ")
            return False
        contrast = int(parts[1])
        for monitor in get_monitors():
            with monitor:
                monitor.set_contrast(contrast)
    except Exception as e:
        await update.message.reply_text(f"Error in setContrastHandler: {e}")

async def setLuminanceHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        parts = update.message.text.split()
        if len(parts) < 2:
            await update.message.reply_text("too short array ")
            return False
        luminance = int(parts[1])
        for monitor in get_monitors():
            with monitor:
                monitor.set_luminance(luminance)
    except Exception as e:
        await update.message.reply_text(f"Error in setLuminanceHandler: {e}")

async def poweroffMonitorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        for monitor in get_monitors():
            with monitor:
                monitor.set_power_mode(4)
    except Exception as e:
        await update.message.reply_text(f"Error in poweroffMonitorHandler: {e}")

async def poweronMonitorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        for monitor in get_monitors():
            with monitor:
                monitor.set_power_mode(1)
    except Exception as e:
        await update.message.reply_text(f"Error in poweronMonitorHandler: {e}")


 

async def volumeUpHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press('up')
    except Exception as e:
        print(f"Error in volumeUpHandler: {e}")

async def volumeDownHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press('down')
    except Exception as e:
        print(f"Error in volumeDownHandler: {e}")

async def rightHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press('right')
    except Exception as e:
        print(f"Error in rightHandler: {e}")

async def leftHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press('left')
    except Exception as e:
        print(f"Error in leftHandler: {e}")

async def closeWindowHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.hotkey('ctrl', 'w')
    except Exception as e:
        print(f"Error in closeWindowHandler: {e}")

async def previousHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.hotkey('shift', 'p')
    except Exception as e:
        print(f"Error in previousHandler: {e}")

async def nextHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.hotkey('shift', 'n')
    except Exception as e:
        print(f"Error in nextHandler: {e}")

async def pauseHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press('space')
    except Exception as e:
        print(f"Error in pauseHandler: {e}")

async def fullHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press('f')
    except Exception as e:
        print(f"Error in fullHandler: {e}")

async def sendKeyHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        command_tmp = update.message.text.split()
        command = command_tmp[1]
        print("received command: " + str(command))
        tab_n = is_number_between_1_and_9(command)
        if tab_n:
            pyautogui.hotkey('ctrl', str(command))
        else:
            pyautogui.typewrite(command)
            pyautogui.press('enter')
    except Exception as e:
        print(f"Error in sendKeyHandler: {e}")

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




#load sensitive data from .env 
#make sure not to push .env to repo

try:
    load_dotenv()
except:
    print("error loading dotenv")

try:
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
except:
    print("error getting TELEGRAM_BOT_TOKEN env var")

try:
    # instantiate app
    app = ApplicationBuilder().token(telegram_token).build()
except:
    print("error instantiatiating app")

unsorted_handlers = {
    "close": closeWindowHandler,
    "down": volumeDownHandler,
    "full": fullHandler,
    "ip": ipHandler,
    "list": sendListHandler,
    "pause": pauseHandler,
    "up": volumeUpHandler,
    "url": urlHandler,
    "c" : sendKeyHandler,
    "right" : rightHandler,
    "left" : leftHandler,
    "previous" : previousHandler,
    "next" : nextHandler,
    "click" : clickHandler,
    "doubleClick" : doubleClickHandler
    # following needs sudo:
    #"poweroff": poweroffHandler,
    #"reboot": rebootHandler,
    #"monitor_data" : monitor_dataHandler,
    #"contrast" : setContrastHandler,
    #"luminance" : setLuminanceHandler,
    #"poweroffMonitor" : poweroffMonitorHandler,
    #"poweronMonitorHandler" : poweronMonitorHandler,
    #"size": screenSizeHandler,
}



# sort handlers list
handlers = dict(sorted(unsorted_handlers.items(), key=lambda item: item[0]))

# default console print color
console_print_color = "cyan"

try:
    #add command handlers
    for comando, manejador in handlers.items():
        app.add_handler(CommandHandler(comando, manejador))
except:
    print("error adding handlers")
try:
    operating_system = get_operating_system()

    print("running on: ", end="")
    print_colored_text(operating_system, console_print_color)
    username = ''
    if(operating_system == 'Linux'):
        username = get_username_linux()
        print("system username running app: ", end="")
        print_colored_text(username, console_print_color)

except:
    print("error getting os")

try:
    host_ip_addr = get_host_ip()
    print("host ip address: ", end="")
    print_colored_text(host_ip_addr, console_print_color)

except:
    print("error getting host ip address ")

print_colored_text("telegram bot started", "magenta")  

try:
    app.run_polling()
except:
    print("error run_polling()")



#username = get_os_username()
