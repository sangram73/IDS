import winreg
import win32api
import win32con
import win32event
import win32security
import win32file
import win32timezone
import time
import threading
import logging

# Setup logger
logging.basicConfig(filename=r"IDS\HIds\logs\registry_changes.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Registry hives to monitor
HIVES = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
}

# Subkeys you want to monitor
SUBKEYS = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
]

def monitor_registry(hive_name, subkey):
    hive = HIVES[hive_name]
    try:
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        key_handle = win32api.RegOpenKeyEx(hive, subkey, 0, win32con.KEY_NOTIFY)
        event = win32event.CreateEvent(None, 0, 0, None)

        while True:
            win32api.RegNotifyChangeKeyValue(
                key_handle,
                True,  # watch subtrees
                win32con.REG_NOTIFY_CHANGE_NAME | win32con.REG_NOTIFY_CHANGE_LAST_SET,
                event,
                True
            )
            win32event.WaitForSingleObject(event, win32con.INFINITE)
            message = f"Registry Change Detected: [{hive_name}\\{subkey}]"
            print(message)
            logging.info(message)

    except Exception as e:
        logging.error(f"Error monitoring {hive_name}\\{subkey}: {str(e)}")

def start_monitoring():
    print("🔍 Starting Windows Registry Monitor...")
    threads = []
    for hive in HIVES:
        for subkey in SUBKEYS:
            thread = threading.Thread(target=monitor_registry, args=(hive, subkey))
            thread.daemon = True
            thread.start()
            threads.append(thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping Registry Monitor...")

if __name__ == "__main__":
    start_monitoring()
