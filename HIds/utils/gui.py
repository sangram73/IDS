import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading
import time

class HIDSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HIDS Security Scanner")
        self.master.geometry("800x500")
        
        # Global variable to track scan status
        self.scanning = False

        # Load icon
        self.icon = PhotoImage(file=r"HIds\utils\favicon-32x32.png")  # Replace with your .png or .gif file path
        self.master.iconphoto(False, self.icon)

        # Load and set background image
        self.bg_image = Image.open(r"HIds\utils\blackbg.png")  # Ensure this image exists in the same directory
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.master, width=800, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10)
        self.style.configure("TLabel", background="#000000", foreground="white", font=("Segoe UI", 16, "bold"))

        # Header
        self.title_label = ttk.Label(self.master, text="🛡️ Host-Based Intrusion Detection System")
        self.canvas.create_window(400, 40, window=self.title_label)

        # Buttons Frame
        self.frame = ttk.Frame(self.master)
        self.canvas.create_window(400, 250, window=self.frame)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        btn_full_scan = ttk.Button(self.frame, text="🧰 Full System Scan", command=lambda: threading.Thread(target=self.full_scan).start())
        btn_file_scan = ttk.Button(self.frame, text="📁 File System Monitor", command=lambda: threading.Thread(target=self.file_scan).start())
        btn_registry_scan = ttk.Button(self.frame, text="🧾 Registry Monitor", command=lambda: threading.Thread(target=self.registry_scan).start())
        btn_network_scan = ttk.Button(self.frame, text="🌐 Network Monitor", command=lambda: threading.Thread(target=self.network_scan).start())
        btn_process_scan = ttk.Button(self.frame, text="⚙️ Process Monitor", command=lambda: threading.Thread(target=self.process_scan).start())
        btn_stop = ttk.Button(self.frame, text="🛑 Stop Scan", command=self.stop_scan)

        btn_full_scan.grid(row=0, column=0, padx=10, pady=10)
        btn_file_scan.grid(row=0, column=1, padx=10, pady=10)
        btn_registry_scan.grid(row=1, column=0, padx=10, pady=10)
        btn_network_scan.grid(row=1, column=1, padx=10, pady=10)
        btn_process_scan.grid(row=2, column=0, columnspan=2, pady=20)
        btn_stop.grid(row=3, column=0, columnspan=2, pady=20)

    def full_scan(self):
        self.scanning = True
        messagebox.showinfo("Full Scan", "Performing full system scan...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Full system scan was aborted.")
                return
            time.sleep(1)  # Simulate work being done
        messagebox.showinfo("Scan Complete", "Full system scan completed.")
        self.scanning = False

    def file_scan(self):
        self.scanning = True
        messagebox.showinfo("File Scan", "Scanning file system for changes...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "File system scan was aborted.")
                return
            time.sleep(1)
        messagebox.showinfo("Scan Complete", "File system scan completed.")
        self.scanning = False

    def registry_scan(self):
        self.scanning = True
        messagebox.showinfo("Registry Scan", "Monitoring Windows registry changes...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Registry monitoring was aborted.")
                return
            time.sleep(1)
        messagebox.showinfo("Scan Complete", "Registry monitoring completed.")
        self.scanning = False

    def network_scan(self):
        self.scanning = True
        messagebox.showinfo("Network Scan", "Analyzing network connections and ports...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Network analysis was aborted.")
                return
            time.sleep(1)
        messagebox.showinfo("Scan Complete", "Network analysis completed.")
        self.scanning = False

    def process_scan(self):
        self.scanning = True
        messagebox.showinfo("Process Scan", "Checking running processes...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Process check was aborted.")
                return
            time.sleep(1)
        messagebox.showinfo("Scan Complete", "Process check completed.")
        self.scanning = False

    def stop_scan(self):
        self.scanning = False

