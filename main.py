#python -m PyInstaller --onefile --name telegram_bot_py.exe --clean main.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import webbrowser
import pyautogui
from dotenv import load_dotenv
import os
import subprocess
import socket
import psutil
import datetime
import pygetwindow as gw
import time
from monitorcontrol import get_monitors

def get_os_username():
    try:
        username = os.getlogin() 
        return username

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def telegramRunningTest():
    processes = [proc.info for proc in psutil.process_iter(['name'])]
    tele_bot_exe_name = "tele_py_bot.exe"
    for process in processes:
        process_name = str(process["name"]).strip()
        if(tele_bot_exe_name == process_name):
            return True
    return False

def chromeRunnnigTest():
    try:
        google_chrome_title_string = "Google Chrome"
        # Obtener todas las ventanas activas
        windows = gw.getAllWindows()
        for window in windows:
            window_title = str(window.title).strip()
            if(window_title != ''):
                if google_chrome_title_string in window_title:
                    return True
        return False
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_partition_info():
    try:
        # Obtener la información sobre las particiones
        partitions = psutil.disk_partitions()

        partition_info = []

        for partition in partitions:
            partition_mountpoint = partition.mountpoint
            partition_device = partition.device
            # Obtener la información sobre el uso de la partición
            usage = psutil.disk_usage(partition_mountpoint)

            # Almacenar la información en un diccionario
            partition_data = {
                'name': partition_device,
                'mountpoint': partition_mountpoint,
                'total_size': format_memory_size(usage.total),
                'used_size': format_memory_size(usage.used),
                'free_size': format_memory_size(usage.free),
                'percent_used': usage.percent
            }

            partition_info.append(partition_data)

        return partition_info

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_cpu_usage():
    try:
        # Obtener la información sobre el uso del CPU
        cpu_usage = psutil.cpu_percent(interval=1)  # interval es el tiempo de espera en segundos

        return cpu_usage

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_memory_usage():
    try:
        # Obtener la información sobre el uso de memoria
        memory_info = psutil.virtual_memory()

        # Obtener la cantidad de memoria RAM utilizada en bytes
        used_memory = memory_info.used

        return used_memory

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_total_memory():
    try:
        # Obtener la información sobre la memoria
        memory_info = psutil.virtual_memory()

        # Obtener la cantidad total de memoria RAM instalada en bytes
        total_memory = memory_info.total

        return total_memory

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def format_memory_size(size_in_bytes):
    # Convertir bytes a kilobytes, megabytes o gigabytes según sea necesario
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0

def get_windows_uptime():
    try:
        # Obtener la información sobre el tiempo de actividad del sistema
        uptime_seconds = psutil.boot_time()

        # Calcular el tiempo de actividad en un formato legible
        uptime_timedelta = datetime.datetime.now() - datetime.datetime.fromtimestamp(uptime_seconds)

        # Obtener los componentes de horas, minutos y segundos
        hours, remainder = divmod(uptime_timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Crear un string formateado
        uptime_string = f"{hours}h {minutes}m {seconds}s"
        
        return uptime_string

    except Exception as e:
        print(f"Error: {e}")
        return None

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
            monitor.set_contrast(luminance)

async def suspendMonitorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for monitor in get_monitors():
        with monitor:
             monitor.set_power_mode("suspend")

 

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
    pyautogui.press('k')

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

async def uptimeUpHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        uptime = str(get_windows_uptime())
        await update.message.reply_text(uptime)
    except:
        print("Error:")

async def systemInfoHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        total_ram = format_memory_size(get_total_memory())
        used_ram = format_memory_size(get_memory_usage())
        reply_text_ram = str(used_ram) + " / " + str(total_ram) + " of memory used"

        cpu_usage = get_cpu_usage()
        reply_text_cpu = str(cpu_usage) + "% cpu usage"

        partitions_info = get_partition_info()
        new_line_char = '\n'
        text_response = reply_text_ram + " " + reply_text_cpu + new_line_char
        if partitions_info is not None:
            for partition in partitions_info:
                text_response += "Partición: " + partition['mountpoint'] + new_line_char
                text_response += "Tamaño total: " + partition['total_size'] + new_line_char
                text_response += "Espacio usado: " + partition['used_size'] + new_line_char
                text_response += "Espacio libre: " + partition['free_size'] + new_line_char
                text_response += "Porcentaje de uso: " + partition['percent_used'] + "%" + new_line_char
        await update.message.reply_text(text_response)
    except:
        print("Error:")

async def cpuInfoInfoHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        cpu_usage = get_cpu_usage()
        reply_text_cpu = str(cpu_usage) + "% cpu usage"
        await update.message.reply_text(reply_text_cpu)

    except:
        print("Error:")

async def memoryInfoInfoHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        total_ram = format_memory_size(get_total_memory())
        used_ram = format_memory_size(get_memory_usage())
        reply_text_ram = str(used_ram) + " / " + str(total_ram) + " of memory used"
        await update.message.reply_text(reply_text_ram)
    except:
        print("Error:")

async def diskInfoInfoHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        partitions_info = get_partition_info()
        if partitions_info is not None:
            for partition in partitions_info:
                await update.message.reply_text(f"Partición: {partition['mountpoint']}")
                await update.message.reply_text(f"Tamaño total: {partition['total_size']}")
                await update.message.reply_text(f"Espacio usado: {partition['used_size']}")
                await update.message.reply_text(f"Espacio libre: {partition['free_size']}")
                await update.message.reply_text(f"Porcentaje de uso: {partition['percent_used']}%")
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


username = get_os_username()
print("telegram bot started by username " + username)

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
    "system_info" : systemInfoHandler,
    "up": volumeUpHandler,
    "uptime": uptimeUpHandler,
    "url": urlHandler,
    "c" : sendKeyHandler,
    "memory" : memoryInfoInfoHandler,
    "disk" : diskInfoInfoHandler,
    "cpu" : cpuInfoInfoHandler,
    "right" : rightHandler,
    "left" : lefttHandler,
    "previous" : previousHandler,
    "next" : nextHandler,
    "monitor_data" : monitor_dataHandler,
    "contrast" : setContrastHandler,
    "luminance" : setLuminanceHandler,
    "suspend" : suspendMonitorHandler
}

handlers = dict(sorted(unsorted_handlers.items(), key=lambda item: item[0]))

#add command handlers
for comando, manejador in handlers.items():
    app.add_handler(CommandHandler(comando, manejador))

app.run_polling()
