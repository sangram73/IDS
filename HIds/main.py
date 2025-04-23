import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import threading
import time
import winreg
from Core.file_monitor import FileSystemMonitor
from Core.process_monitor import ProcessMonitor
from Core.network_monitor import NetworkMonitor
from Core.registry_monitor import RegistryMonitor
from alert_manager import show_alert, show_warning
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

watch_dir = r""
log_file = r"HIds\logs\file_changes.log"
snapshot_file = r"HIds\logs\snapshot.json"
# ------------------------------------ Registry Var----------
HIVES = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
}
SUBKEYS = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"]
LOG_PATH = r"HIds\\logs\\registry_changes.log"


class HIDSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("LiveShield-HIDS Security Scanner")
        self.master.geometry("800x500")
        self.icon = ImageTk.PhotoImage(file=r"HIds\utils\favicon-32x32.png")
        self.master.iconphoto(False, self.icon)

        self.master.configure(bg="#000000")
        self.scanning = False
        self.network_monitor = None  # To hold the network monitor instance

        self.bg_image = Image.open(r"HIds\utils\bg_new.jpg")
        img=self.bg_image.resize((800, 500))
        self.bg_photo = ImageTk.PhotoImage(img)
        self.background_label = tk.Label(master, image=self.bg_photo, bg="#000000")
        self.background_label.image = self.bg_photo
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10, relief="flat", background="#0078d7", foreground="black")
        self.style.map("TButton", background=[("active", "#0056a3")], foreground=[("active", "white")])
        self.style.configure("TLabel", background="#000000", foreground="white", font=("Segoe UI", 16, "bold"))

        # self.title_label = ttk.Label(master, text="LiveShield" ,background="black", foreground="black")
        # self.title_label.place(relx=0.5, rely=0.05, anchor='center')

        #self.create_left_section()
        self.create_buttons()
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        menu1 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu1.add_command(label="Option 1", command=lambda: self.show_message("Menu 1 - Option 1"))
        menu1.add_command(label="Option 2", command=lambda: self.show_message("Menu 1 - Option 2"))
        menu_bar.add_cascade(label="File", menu=menu1)

        menu2 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu2.add_command(label="Option 1", command=lambda: self.show_message("Menu 2 - Option 1"))
        menu2.add_command(label="Option 2", command=lambda: self.show_message("Menu 2 - Option 2"))
        menu_bar.add_cascade(label="Logs", menu=menu2)

        menu3 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu3.add_command(label="Option 1", command=lambda: self.show_message("Menu 3 - Option 1"))
        menu3.add_command(label="Option 2", command=lambda: self.show_message("Menu 3 - Option 2"))
        menu_bar.add_cascade(label="Config", menu=menu3)

        menu4 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu4.add_command(label="Option 1", command=lambda: self.show_message("Menu 4 - Option 1"))
        menu4.add_command(label="Option 2", command=lambda: self.show_message("Menu 4 - Option 2 "))
        menu_bar.add_cascade(label="Alert", menu=menu4)

        self.master.config(menu=menu_bar)

    def show_message(self, message):
        messagebox.showinfo("Menu Selection", message)

    def create_buttons(self):
        button_frame = ttk.Frame(self.master, style="TFrame", padding=(10, 10))
        button_frame.place(relx=0.45, rely=0.18, relwidth=0.53, relheight=0.64)

        btn_full_scan = ttk.Button(button_frame, text="🧰 Full Scan",bootstyle="primary,outline", command=lambda: threading.Thread(target=self.full_scan).start())
        btn_file_scan = ttk.Button(button_frame, text="📁 File Scan",bootstyle="primary,outline", command=lambda: threading.Thread(target=self.file_scan).start())
        btn_registry_scan = ttk.Button(button_frame, text="🧾 Registry Scan",bootstyle="primary,outline", command=lambda: threading.Thread(target=self.registry_scan).start())
        btn_network_scan = ttk.Button(button_frame, text="🌐 Network Scan",bootstyle="primary,outline", command=lambda: threading.Thread(target=self.network_scan).start())
        btn_process_scan = ttk.Button(button_frame, text="⚙️ Process Scan",bootstyle="primary,outline", command=lambda: threading.Thread(target=self.process_scan).start())
        btn_stop = ttk.Button(button_frame, text="🛑 Stop Scan",bootstyle="primary,outline", command=self.stop_scan)

        btn_prev_report = ttk.Button(button_frame, text=" 🔍 See Previous Scan Report",bootstyle="primary,outline", command=self.show_prev_report)
        btn_review_log = ttk.Button(button_frame, text="📄 Review Log",bootstyle="primary,outline", command=self.review_log)

        btn_process_scan.grid(row=0, column=0, padx=5, pady=10, sticky='ew')
        btn_file_scan.grid(row=0, column=1, padx=5, pady=10, sticky='ew')
        btn_registry_scan.grid(row=1, column=0, padx=5, pady=10, sticky='ew')
        btn_network_scan.grid(row=1, column=1, padx=5, pady=10, sticky='ew')
        btn_full_scan.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
        btn_stop.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        btn_prev_report.grid(row=4, column=0, padx=5, pady=10, sticky='ew')
        btn_review_log.grid(row=4, column=1, padx=5, pady=10, sticky='ew')

    # def create_left_section(self):
    #     self.logo_image = Image.open(r"IDS\HIds\utils\logo1.png")
    #     self.logo_photo = ImageTk.PhotoImage(self.logo_image)
    #     logo_label = ttk.Label(self.master, image=self.logo_photo, background="#1f1d1d")
    #     logo_label.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.35)

    def show_prev_report(self):
        messagebox.showinfo("Previous Scan Report", "Displaying previous scan report...")

    def review_log(self):
        # Create a new window for reviewing the log
        log_window = tk.Toplevel(self.master)
        log_window.title("Log Review")
        log_window.geometry("600x400")

        # Create a Text widget to display the log contents
        log_text = tk.Text(log_window, wrap=tk.WORD)
        log_text.pack(expand=True, fill=tk.BOTH)

        # Add a scrollbar to the Text widget
        scrollbar = tk.Scrollbar(log_window, command=log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.config(yscrollcommand=scrollbar.set)

        # Read the log file and insert its contents into the Text widget
        try:
            with open(log_file, 'r') as file:
                log_contents = file.read()
                log_text.insert(tk.END, log_contents)
        except FileNotFoundError:
            log_text.insert(tk.END, "Log file not found.")
        except Exception as e:
            log_text.insert(tk.END, f"An error occurred: {str(e)}")

        # Make the Text widget read-only
        log_text.config(state=tk.DISABLED)

    # def full_scan(self):
    #     self.scanning = True
    #     messagebox.showinfo("Full Scan", "Performing full system scan...")
        
    #     # Call each scan method sequentially
    #     self.process_scan()
    #     if not self.scanning:
    #         return

    #     self.registry_scan()
    #     if not self.scanning:
    #         return
        
    #     self.network_scan()
    #     if not self.scanning:
    #         self.stop_scan()
    #         return
        
    #     self.file_scan()
    #     if not self.scanning:
    #         self.stop_scan()
    #         return
    #     messagebox.showinfo("Scan Complete", "Full system scan completed.")

    def full_scan(self):
        threading.Thread(target=self._full_scan_logic).start()

    def _full_scan_logic(self):
        self.scanning = True
        show_alert("Full Scan, Performing full system scan...")

        self._process_scan_sync()
        if not self.scanning: return

        self._registry_scan_sync()
        if not self.scanning: return

        self._network_scan_sync()
        if not self.scanning: return

        self._file_scan_sync()
        if not self.scanning: return

        show_alert("Scan Complete, Full system scan completed.")

# --------- SYNC versions of scan methods (used only in full_scan) ----------

    def _process_scan_sync(self):   
        monitor = ProcessMonitor()
        monitor.process_scan()

    def _registry_scan_sync(self):  
        DURATION = 5
        monitor = RegistryMonitor(LOG_PATH, HIVES, SUBKEYS, DURATION)
        monitor.start_monitoring()
        for i in range(5):
            if not self.scanning:
                return
            time.sleep(1)

    def _network_scan_sync(self):   
        self.network_monitor = NetworkMonitor("Intel(R) Wi-Fi 6E AX211 160MHz")  # Or auto-select
        self.network_monitor.start_sniffing()
        for i in range(5):
            if not self.scanning:
                self.network_monitor.stop_sniffing()
                return
            time.sleep(1)
        self.network_monitor.stop_sniffing()

    def _file_scan_sync(self):
        # Choose default or predefined directory instead of GUI interaction
        directory = r"C:\Users\KIIT0001\Downloads"  # You could auto-configure this or add a parameter
        monitor = FileSystemMonitor(watch_dir=directory, log_file=log_file, snapshot_file=snapshot_file)
        monitor.start_monitoring()
        for i in range(5):
            if not self.scanning:
               return
            time.sleep(1)


    def file_scan(self):
            directory = filedialog.askdirectory(title="Select Directory to Scan")
            monitor = FileSystemMonitor(watch_dir=directory, log_file=log_file, snapshot_file=snapshot_file)
            if directory:
                self.scanning = True
                messagebox.showinfo("File Scan", f"Scanning directory: {directory}...")
                monitor.start_monitoring()
                for i in range(5):
                    if not self.scanning:
                        messagebox.showinfo("Scan Aborted", "File system scan was aborted.")
                        return
                    time.sleep(1)  # Simulate work being done
                messagebox.showinfo("Scan Complete", "File system scan completed.")

    def registry_scan(self):
        self.scanning = True
        messagebox.showinfo("Registry Scan", "Monitoring Windows registry changes...")

    # Define a function for the monitoring
        def monitor_registry():
            # Duration in seconds (e.g., 60 for 1 minute)
            DURATION = 5
            monitor = RegistryMonitor(LOG_PATH, HIVES, SUBKEYS, DURATION)
            monitor.start_monitoring()

            # Simulate work with sleep
            for i in range(5):
                if not self.scanning:
                    self.after(0, lambda: messagebox.showinfo("Scan Aborted", "Registry monitoring was aborted."))
                    return
                time.sleep(1)  # Simulate work being done

            # After completion, make sure to call the messagebox on the main thread
            self.after(0, lambda: messagebox.showinfo("Scan Complete", "Registry monitoring completed."))
            self.scanning = False

        # Run the monitor_registry function in a separate thread
        threading.Thread(target=monitor_registry, daemon=True).start()

    def network_scan(self):
        interfaces = [
            "Intel(R) Wi-Fi 6E AX211 160MHz",
            "Microsoft IP-HTTPS Platform Adapter",
            "Microsoft 6to4 Adapter",
            "Bluetooth Device (Personal Area Network)",
            "Microsoft Kernel Debug Network Adapter"
        ]

        dropdown_window = tk.Toplevel()
        dropdown_window.title("Select Network Interface")
        dropdown_window.configure(bg="#f0f0f0")

        tk.Label(dropdown_window, text="Select Network Interface:", font=("Segoe UI", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        selected_interface = tk.StringVar(dropdown_window)
        selected_interface.set(interfaces[0])  # Default selection

        dropdown = tk.OptionMenu(dropdown_window, selected_interface, *interfaces)
        dropdown.config(
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#333333",
            activebackground="#cce5ff",
            width=40,
            relief=tk.GROOVE
        )
        dropdown["menu"].config(font=("Segoe UI", 10), bg="white", fg="#000000", activebackground="#cce5ff")
        dropdown.pack(pady=5)

        def scan_logic():
            self.scanning = True
            self.network_monitor = NetworkMonitor(selected_interface.get())
            self.network_monitor.start_sniffing()
            messagebox.showinfo("Network Scan", f"Analyzing {selected_interface.get()} and ports...")
            for i in range(5):
                if not self.scanning:
                    messagebox.showinfo("Scan Aborted", "Network analysis was aborted.")
                    self.network_monitor.stop_sniffing()  # Stop the network monitor
                    return
                time.sleep(1)  # Simulate work
            self.scanning = False
        tk.Button(dropdown_window, text="Start Scan", command=lambda: threading.Thread(target=scan_logic).start()).pack(pady=10)

    def process_scan(self):
        monitor = ProcessMonitor()
        monitor.process_scan()

    def stop_scan(self):
        self.scanning = False
        if self.network_monitor:
            self.network_monitor.stop_sniffing()  # Stop the network monitor if it's running
       

root = tk.Tk()
app = HIDSApp(root)
root.mainloop()