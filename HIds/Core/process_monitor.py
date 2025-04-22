import psutil
import csv
import time
from tkinter import messagebox

class ProcessMonitor:
    
    def __init__(self):
        self.scanning = False
        self.malicious_processes = self.load_malicious_processes('HIds/logs/blacklisted_Processes.csv')

    def load_malicious_processes(self, file_path):
        malicious_processes = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                malicious_processes.append(row['keyword'])
        return malicious_processes

    def check_running_processes(self):
        detected_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in self.malicious_processes:
                    detected_processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return detected_processes

    def process_scan(self):
        self.scanning = True
        messagebox.showinfo("Process Scan", "Checking running processes...")
        
        # Simulate work being done
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Process check was aborted.")
                return
            time.sleep(1)  # Simulate work being done
        
        # Check for malicious processes
        detected_processes = self.check_running_processes()
        self.scanning = False
        
        # Prepare the result message
        if detected_processes:
            result_message = "Malicious Processes Detected:\n" + "\n".join(detected_processes)
        else:
            result_message = "No malicious processes detected."
        
        messagebox.showinfo("Scan Complete", result_message)

# Example usage in a GUI application
if __name__ == "__main__":
    # Initialize your GUI and create an instance of ProcessMonitor
    monitor = ProcessMonitor()
    monitor.process_scan() 
    # Call  when the user clicks the button to start the scan