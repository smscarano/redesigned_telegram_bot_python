from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import webbrowser
import pyautogui
from dotenv import load_dotenv
import os
import socket
import time
import platform
from datetime import datetime,timedelta

# options list

options = {
    # default console print color
    "console_print_color": "yellow"
}

script_start_datetime = datetime.now()

def osData():
    try:
        operating_system = get_operating_system()
        print("host os: ", end="")
        print_colored_text(
            operating_system.upper(), options["console_print_color"], bold=True
        )
        username = ""
        if operating_system == "Linux":
            distro_data = get_linux_distro()
            print("linux distribution: ", end="")
            print_colored_text(distro_data, options["console_print_color"], bold=True)

            username = get_username_linux()
            print("system username: ", end="")
            print_colored_text(username, options["console_print_color"], bold=True)
    except:
        print("error getting os")

def initDataPrint():
    try:
        print("started at: ", end="")
        print_colored_text(get_formatted_current_datetime(), options["console_print_color"], bold=True)
    except:
        print("error printing get_formatted_current_datetime()")

    try:
        osData()
    except:
        print("error running osData()")

    try:
        host_ip_addr = get_host_ip()
        print("host ip address: ", end="")
        print_colored_text(host_ip_addr, options["console_print_color"], bold=True)

    except:
        print("error getting host ip address ")

    bot_started_msg = "telegram bot started"
    print_colored_text(bot_started_msg.upper(), "green", bold=True)

def get_formatted_current_datetime():
    try:
        # Get current date and time
        current_datetime = datetime.now()

        # Format the date and time as dd/mm/yyyy hh:mm:ss
        formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

        return formatted_datetime

    except Exception as e:
        print(f"Error in get_formatted_current_datetime: {e}")
        return None


def get_operating_system():
    try:
        system_name = platform.system()
        return system_name
    except Exception as e:
        print(f"Error getting operating system: {e}")
        return None


# Get the Linux distribution information using distro module
def get_linux_distro():
    try:
        import distro

        # Format the information
        distro_name = distro.name().strip()
        distro_version = distro.version().strip()

        # Return the formatted string
        return f"{distro_name} {distro_version}"

    except Exception as e:
        return f"Error getting Linux distribution: {e}"


def get_username_linux():
    try:
        username = os.getenv("USER") or os.getenv("LOGNAME") or os.getenv("USERNAME")
        return username
    except Exception as e:
        print(f"Error getting username on Linux: {e}")
        return None


def get_username_windows():
    try:
        username = os.getenv("USERNAME")
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


def print_colored_text(text, color_name, bold=False):
    try:
        color_codes = {
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37,
        }
        # Check if the specified color is in the dictionary
        if color_name not in color_codes:
            raise ValueError(f"Invalid color: {color_name}")

        color_code = color_codes[color_name]

        # Add bold style if bold is True
        bold_code = "1" if bold else ""

        # Print colored text using ANSI escape codes
        print(f"\033[{bold_code};{color_code}m{text}\033[0m")

    except:
        print("Error calling print_colored_text()")


async def sendListHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global handlers
    try:
        command_list = "\n".join([f"/{comando}" for comando, _ in handlers.items()])
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


async def volumeUpHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press("up")
    except Exception as e:
        print(f"Error in volumeUpHandler: {e}")


async def volumeDownHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press("down")
    except Exception as e:
        print(f"Error in volumeDownHandler: {e}")


async def rightHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press("right")
    except Exception as e:
        print(f"Error in rightHandler: {e}")


async def leftHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press("left")
    except Exception as e:
        print(f"Error in leftHandler: {e}")


async def closeWindowHandler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        pyautogui.hotkey("ctrl", "w")
    except Exception as e:
        print(f"Error in closeWindowHandler: {e}")


async def previousHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.hotkey("shift", "p")
    except Exception as e:
        print(f"Error in previousHandler: {e}")


async def nextHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.hotkey("shift", "n")
    except Exception as e:
        print(f"Error in nextHandler: {e}")


async def pauseHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press("space")
    except Exception as e:
        print(f"Error in pauseHandler: {e}")


async def fullHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.press("f")
    except Exception as e:
        print(f"Error in fullHandler: {e}")

async def poweroffHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global script_start_datetime
        # Get the current datetime
        current_datetime = datetime.now()

        # Assuming script_start_datetime is defined somewhere earlier
        # Calculate the elapsed time since script_start_datetime
        elapsed_time = current_datetime - script_start_datetime

        # Check if 10 seconds have passed since script started
        if elapsed_time >= timedelta(seconds=10):
            operating_system = get_operating_system()
            if operating_system == "Linux":
                print("poweroff")
                os.system('sudo poweroff')

    except Exception as e:
        print(f"Error in poweroffHandler: {e}")

async def sendKeyHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        command_tmp = update.message.text.split()
        command = command_tmp[1]
        tab_n = is_number_between_1_and_9(command)
        if tab_n:
            pyautogui.hotkey("ctrl", str(command))
        else:
            pyautogui.typewrite(command)
            pyautogui.press("enter")
    except Exception as e:
        print(f"Error in sendKeyHandler: {e}")
        await update.message.reply_text(str(e))


async def ipHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        ip_address = str(get_host_ip())
        await update.message.reply_text(ip_address)
    except:
        print("Error:")


async def screenSizeHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        size = pyautogui.size()
        await update.message.reply_text(str(size[0]) + " " + str(size[1]))

    except:
        print("Error:")


async def clickHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.click()
    except:
        print("Error:")


async def doubleClickHandler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        pyautogui.click(2, interval=0.1)
    except:
        print("Error:")

# ... (after handlers are added)
# load sensitive data from .env
# make sure not to push .env to repo
try:
    load_dotenv()
except:
    print("error loading dotenv")

try:
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
except:
    print("error getting TELEGRAM_BOT_TOKEN env var")

# instantiate app
try:
    app = ApplicationBuilder().token(telegram_token).build()

except:
    print("error instantiatiating app")

# handlers list
unsorted_handlers = {
    "close": closeWindowHandler,
    "down": volumeDownHandler,
    "full": fullHandler,
    "ip": ipHandler,
    "list": sendListHandler,
    "pause": pauseHandler,
    "up": volumeUpHandler,
    "url": urlHandler,
    "c": sendKeyHandler,
    "right": rightHandler,
    "left": leftHandler,
    "previous": previousHandler,
    "next": nextHandler,
    "click": clickHandler,
    "doubleClick": doubleClickHandler,
    
    # following needs sudo:
    "poweroff": poweroffHandler
    # "reboot": rebootHandler,
    # "monitor_data" : monitor_dataHandler,
    # "contrast" : setContrastHandler,
    # "luminance" : setLuminanceHandler,
    # "poweroffMonitor" : poweroffMonitorHandler,
    # "poweronMonitorHandler" : poweronMonitorHandler,
    # "size": screenSizeHandler,
}

# sorted handlers list
handlers = dict(sorted(unsorted_handlers.items(), key=lambda item: item[0]))

# add command handlers
try:
    for command, handler in handlers.items():
        app.add_handler(CommandHandler(command, handler))
except:
    print("error adding handlers")

try:
    initDataPrint()
except:
    print("error initDataPrint()")

try:
    app.run_polling()
except Exception as e:
    print_colored_text("error run_polling()", "red")
    print_colored_text(str(e), "red")
