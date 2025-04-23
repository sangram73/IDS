import win32api
import winreg
import win32con
import win32event
import logging
import time
import threading
from alert_manager import show_alert, show_warning

class RegistryMonitor:
    def __init__(self, log_path, hives, subkeys, duration=None):
        self.log_path = log_path
        self.hives = hives
        self.subkeys = subkeys
        self.duration = duration  # Duration in seconds
        self.stop_event = threading.Event()
        logging.basicConfig(filename=self.log_path, level=logging.INFO, format="%(asctime)s - %(message)s")

    def monitor_key(self, hive_name, subkey):
        hive = self.hives[hive_name]
        try:
            key_handle = win32api.RegOpenKeyEx(hive, subkey, 0, win32con.KEY_NOTIFY)
            event = win32event.CreateEvent(None, 0, 0, None)

            while not self.stop_event.is_set():
                win32api.RegNotifyChangeKeyValue(
                    key_handle,
                    True,
                    win32con.REG_NOTIFY_CHANGE_NAME | win32con.REG_NOTIFY_CHANGE_LAST_SET,
                    event,
                    True
                )
                result = win32event.WaitForSingleObject(event, 1000)  # Wait max 1 second, then check stop_event
                if result == win32con.WAIT_OBJECT_0:
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
            if self.duration:
                time.sleep(self.duration)
                self.stop_event.set()
                print("no changes detected")
                show_warning(f"🛑 Monitoring stopped after {self.duration} seconds.")
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop_event.set()
            show_warning("🛑 Registry Monitor Stopped by user.")

# if __name__ == "__main__":
#     HIVES = {
#         "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
#         "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
#     }
#     SUBKEYS = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"]
#     LOG_PATH = r"IDS\HIds\\logs\\registry_changes.log"

#     # Duration in seconds (e.g., 60 for 1 minute)
#     DURATION = 10

#     monitor = RegistryMonitor(LOG_PATH, HIVES, SUBKEYS, duration=DURATION)
#     monitor.start_monitoring()