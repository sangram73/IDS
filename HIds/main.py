import threading
import time
import tkinter as tk
from Core.file_monitor import FileSystemMonitor
from Core.process_monitor import ProcessMonitor
from Core.registry_monitor import RegistryMonitor
from Core.network_monitor import NetworkMonitor
from utils.gui import HIDSApp


import scapy.all as scapy
import winreg

# --------------------------------- File Monitor var--------
watch_dir = r"C:\\Users\\KIIT0001\\Pictures"
log_file = r"HIds\\logs\\file_changes.log"
snapshot_file = r"HIds\\logs\\snapshot.json"

# ------------------------------------ Registry Var----------
HIVES = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
}
SUBKEYS = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"]
LOG_PATH = r"HIds\\logs\\registry_changes.log"

# ------------------------------------ Network Var----------
def alert_and_stop():
    print("ALERT! Suspicious activity detected! Stopping all monitors...")
    global running
    running = False

def monitor_file_system():
    monitor = FileSystemMonitor(watch_dir, log_file, snapshot_file)
    monitor.start_monitoring()

def monitor_processes():
    process_monitor = ProcessMonitor()
    while running:
        process_monitor.get_running_processes()
        time.sleep(5)  # Check every 5 seconds

def monitor_registry():
    monitor = RegistryMonitor(LOG_PATH, HIVES, SUBKEYS)
    monitor.start_monitoring()

def monitor_network():
    scapy.show_interfaces()
    interface = input("Enter interface: ")
    network_monitor = NetworkMonitor(interface)
    network_monitor.start_sniffing()

def stop_monitoring():
    global running
    running = False
    print("Stopping all monitors...")

def main():
    root = tk.Tk()
    app = HIDSApp(root)
    root.mainloop()

    global running
    running = True
    
    # Start monitoring threads
    file_thread = threading.Thread(target=monitor_file_system)
    process_thread = threading.Thread(target=monitor_processes)
    registry_thread = threading.Thread(target=monitor_registry)
    network_thread = threading.Thread(target=monitor_network)

    file_thread.start()
    process_thread.start()
    registry_thread.start()
    network_thread.start()

    # User input loop for stopping the monitoring
    while running:
        user_input = input("Type 'stop' to abort monitoring: ")
        if user_input.lower() == 'stop':
            stop_monitoring()

    # Wait for all threads to finish
    file_thread.join()
    process_thread.join()
    registry_thread.join()
    network_thread.join()

if __name__ == "__main__":
    main()