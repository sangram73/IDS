import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading
import time

# Global variable to track scan status
scanning = False

# Stub scan functions (replace with actual HIDS functionality)
def full_scan():
    global scanning
    scanning = True
    messagebox.showinfo("Full Scan", "Performing full system scan...")
    # Simulate a long-running scan
    for i in range(5):
        if not scanning:
            messagebox.showinfo("Scan Aborted", "Full system scan was aborted.")
            return
        time.sleep(1)  # Simulate work being done
    messagebox.showinfo("Scan Complete", "Full system scan completed.")
    scanning = False

def file_scan():
    global scanning
    scanning = True
    messagebox.showinfo("File Scan", "Scanning file system for changes...")
    for i in range(5):
        if not scanning:
            messagebox.showinfo("Scan Aborted", "File system scan was aborted.")
            return
        time.sleep(1)
    messagebox.showinfo("Scan Complete", "File system scan completed.")
    scanning = False

def registry_scan():
    global scanning
    scanning = True
    messagebox.showinfo("Registry Scan", "Monitoring Windows registry changes...")
    for i in range(5):
        if not scanning:
            messagebox.showinfo("Scan Aborted", "Registry monitoring was aborted.")
            return
        time.sleep(1)
    messagebox.showinfo("Scan Complete", "Registry monitoring completed.")
    scanning = False

def network_scan():
    global scanning
    scanning = True
    messagebox.showinfo("Network Scan", "Analyzing network connections and ports...")
    for i in range(5):
        if not scanning:
            messagebox.showinfo("Scan Aborted", "Network analysis was aborted.")
            return
        time.sleep(1)
    messagebox.showinfo("Scan Complete", "Network analysis completed.")
    scanning = False

def process_scan():
    global scanning
    scanning = True
    messagebox.showinfo("Process Scan", "Checking running processes...")
    for i in range(5):
        if not scanning:
            messagebox.showinfo("Scan Aborted", "Process check was aborted.")
            return
        time.sleep(1)
    messagebox.showinfo("Scan Complete", "Process check completed.")
    scanning = False

def stop_scan():
    global scanning
    scanning = False

# GUI Setup
root = tk.Tk()
root.title("HIDS Security Scanner")
root.geometry("800x500")

# Replace with your .png or .gif file path
icon = PhotoImage(file=r"HIds\utils\favicon-32x32.png")  # Replace with your .png or .gif file path
root.iconphoto(False, icon)

# Load and set background image
bg_image = Image.open(r"HIds\utils\blackbg.png")  # Ensure this image exists in the same directory
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=800, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12), padding=10)
style.configure("TLabel", background="#000000", foreground="white", font=("Segoe UI", 16, "bold"))

# Header
title_label = ttk.Label(root, text="🛡️ Host-Based Intrusion Detection System")
title_window = canvas.create_window(400, 40, window=title_label)

# Buttons Frame
frame = ttk.Frame(root)
frame_window = canvas.create_window(400, 250, window=frame)

# Buttons
btn_full_scan = ttk.Button(frame, text="🧰 Full System Scan", command=lambda: threading.Thread(target=full_scan).start())
btn_file_scan = ttk.Button(frame, text="📁 File System Monitor", command=lambda: threading.Thread(target=file_scan).start())
btn_registry_scan = ttk.Button(frame, text="🧾 Registry Monitor", command=lambda: threading.Thread(target=registry_scan).start())
btn_network_scan = ttk.Button(frame, text="🌐 Network Monitor", command=lambda: threading.Thread(target=network_scan).start())
btn_process_scan = ttk.Button(frame, text="⚙️ Process Monitor", command=lambda: threading.Thread(target=process_scan).start())
btn_stop = ttk.Button(frame, text="🛑 Stop Scan", command=stop_scan)

btn_full_scan.grid(row=0, column=0, padx=10, pady=10)
btn_file_scan.grid(row=0, column=1, padx=10, pady=10)
btn_registry_scan.grid(row=1, column=0, padx=10, pady=10)
btn_network_scan.grid(row=1, column=1, padx=10, pady=10)
btn_process_scan.grid(row=2, column=0, columnspan=2, pady=20)
btn_stop.grid(row=3, column=0, columnspan=2, pady=20)

# Run the GUI
root.mainloop()