import subprocess
from monitorcontrol import get_monitors


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