import tkinter as tk
import psutil
from alert_manager import show_alert
import pandas

def get_running_processes():
    running_processes = []
    malicious_keywords = pandas.read_csv(r"C:\Study\MajorProject\IDS\HIds\logs\blacklisted_Processes.csv")
    for process in psutil.process_iter(attrs=['pid', 'name']):
        process_name = process.info['name']
        process_id = process.info['pid']
        running_processes.append((process_id, process_name))

        try:          
            if any(keyword in process_name.lower() for keyword in malicious_keywords):
                print(f"ALERT! Suspicious Process Detected: {process_name}")
                show_alert("ALERT! Suspicious Process Detected: {process_name}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    with open("C:\\Study\\MajorProject\\IDS\\HIds\\logs\\process_log.log","w") as log_file:

        for pid, name in running_processes:
            print(pid,name)
            log_file.write(f"{pid}: {name}\n")
    return running_processes

get_running_processes()


