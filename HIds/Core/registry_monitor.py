import win32api
import winreg
import win32con
import win32event
import logging
import time
import threading
from alert_manager import show_alert, show_warning

class RegistryMonitor:
    def __init__(self, log_path, hives, subkeys):
        self.log_path = log_path
        self.hives = hives
        self.subkeys = subkeys
        logging.basicConfig(filename=self.log_path, level=logging.INFO, format="%(asctime)s - %(message)s")

    def monitor_key(self, hive_name, subkey):
        hive = self.hives[hive_name]
        try:
            key_handle = win32api.RegOpenKeyEx(hive, subkey, 0, win32con.KEY_NOTIFY)
            event = win32event.CreateEvent(None, 0, 0, None)

            while True:
                win32api.RegNotifyChangeKeyValue(
                    key_handle,
                    True,
                    win32con.REG_NOTIFY_CHANGE_NAME | win32con.REG_NOTIFY_CHANGE_LAST_SET,
                    event,
                    True
                )
                win32event.WaitForSingleObject(event, win32con.INFINITE)
                message = f"[ALERT] Registry Change Detected: [{hive_name}\\{subkey}]"
                show_warning(message)
                logging.info(message)

        except Exception as e:
            logging.error(f"Error monitoring {hive_name}\\{subkey}: {str(e)}")

    def start_monitoring(self):
        print("🔍 Starting Registry Monitor...")
        threads = []
        for hive in self.hives:
            for subkey in self.subkeys:
                thread = threading.Thread(target=self.monitor_key, args=(hive, subkey))
                thread.daemon = True
                thread.start()
                threads.append(thread)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            show_warning("🛑 Registry Monitor Stopped.")


if __name__ == "__main__":
    HIVES = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
 }
    SUBKEYS = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"]
    LOG_PATH = r"HIds\\logs\\registry_changes.log"
    # Initialize your GUI and create an instance of ProcessMonitor
    monitor = RegistryMonitor(LOG_PATH,HIVES,SUBKEYS)
    monitor.start_monitoring() 



