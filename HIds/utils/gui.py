import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import threading
import time

class HIDSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HIDS Security Scanner")
        self.master.geometry("800x500")
        self.icon =ImageTk.PhotoImage(file=r"HIds\utils\favicon-32x32.png")  # Replace with your .png or .gif file path
        self.master.iconphoto(False, self.icon)

        # Set the background color of the main window to black
        self.master.configure(bg="#000000")

        # Global variable to track scan status
        self.scanning = False

        # Load and set background image
        self.bg_image = Image.open("HIds/utils/blackbg.png")  # Ensure this image exists in the same directory
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set the background image on the main window
        self.background_label = tk.Label(master, image=self.bg_photo, bg="#000000")
        self.background_label.image = self.bg_photo  # Keep a reference to avoid garbage collection
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10, relief="flat", background="#0078d7", foreground="black")
        self.style.map("TButton", background=[("active", "#0056a3")], foreground=[("active", "white")])  # Change color on hover
        self.style.configure("TLabel", background="#000000", foreground="white", font=("Segoe UI", 16, "bold"))

        # Header
        self.title_label = ttk.Label(master, text="Host-Based Intrusion Detection System")
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')  # Center the title at the top

        # Create the left section for logo and buttons
        self.create_left_section()

        # Create the right section for buttons
        self.create_buttons()

        # Create the menu bar
        self.create_menu()

    def create_menu(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.master)

        # Create the first menu
        menu1 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu1.add_command(label="Option 1", command=lambda: self.show_message("Menu 1 - Option 1"))
        menu1.add_command(label="Option 2", command=lambda: self.show_message("Menu 1 - Option 2"))
        menu_bar.add_cascade(label="Menu 1", menu=menu1)

        # Create the second menu
        menu2 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu2.add_command(label="Option 1", command=lambda: self.show_message("Menu 2 - Option 1"))
        menu2.add_command(label="Option 2", command=lambda: self.show_message("Menu 2 - Option 2"))
        menu_bar.add_cascade(label="Menu 2", menu=menu2)

        # Create the third menu
        menu3 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu3.add_command(label="Option 1", command=lambda: self.show_message("Menu 3 - Option 1"))
        menu3.add_command(label="Option 2", command=lambda: self.show_message("Menu 3 - Option 2"))
        menu_bar.add_cascade(label="Menu 3", menu=menu3)

        # Create the fourth menu
        menu4 = tk.Menu(menu_bar, tearoff=0, bg="#0099cc", fg="black")
        menu4.add_command(label="Option 1", command=lambda: self.show_message("Menu 4 - Option 1"))
        menu4.add_command(label="Option 2", command=lambda: self.show_message("Menu 4 - Option 2"))
        menu_bar.add_cascade(label="Menu 4", menu=menu4)

        # Configure the menu bar
        self.master.config(menu=menu_bar)

    def show_message(self, message):
        messagebox.showinfo("Menu Selection", message)

    def create_buttons(self):
        # Create a frame for buttons with increased width
        button_frame = ttk.Frame (self.master, style="TFrame", padding=(10, 10))
        button_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.8)  # Increased relwidth

        btn_full_scan = ttk.Button(button_frame, text="🧰 Full Scan", command=lambda: threading.Thread(target=self.full_scan).start())
        btn_file_scan = ttk.Button(button_frame, text="📁 File Scan", command=lambda: threading.Thread(target=self.file_scan).start())
        btn_registry_scan = ttk.Button(button_frame, text="🧾 Registry Scan", command=lambda: threading.Thread(target=self.registry_scan).start())
        btn_network_scan = ttk.Button(button_frame, text="🌐 Network Scan", command=lambda: threading.Thread(target=self.network_scan).start())
        btn_process_scan = ttk.Button(button_frame, text="⚙️ Process Scan", command=lambda: threading.Thread(target=self.process_scan).start())
        btn_stop = ttk.Button(button_frame, text="🛑 Stop Scan", command=self.stop_scan)

        # Arrange buttons in a grid with proper alignment
        btn_full_scan.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        btn_file_scan.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        btn_registry_scan.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        btn_network_scan.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        btn_process_scan.grid(row=2, column=0, columnspan=2, padx=5, pady=20, sticky='ew')
        btn_stop.grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky='ew')

        # Configure column weights to ensure proper alignment
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
# feture style propoties
    # def create_rounded_button(self, parent, text, command):
    #     button_canvas = tk.Canvas(parent, width=200, height=50, bg="#0078d7", highlightthickness=0, borderwidth=0)
    #     button_canvas.create_oval(0, 0, 20, 50, fill="#0078d7", outline="#0078d7")
    #     button_canvas.create_oval(180, 0, 200, 50, fill="#0078d7", outline="#0078d7")
    #     button_canvas.create_rectangle(20, 0, 180, 50, fill="#0078d7", outline="#0078d7")
    #     button_canvas.create_text(100, 25, text=text, fill="black", font=("Segoe UI", 12))
    #     button_canvas.bind("<Button-1>", lambda e: command())
    #     button_canvas.pack(pady=10)

    def create_left_section(self):
        # Load and display the logo
        self.logo_image = Image.open("HIds/utils/logo1.png")  # Ensure this image exists in the same directory
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        logo_label = ttk.Label(self.master, image=self.logo_photo, background="#1f1d1d")
        logo_label.place(relx=0.1, rely=0.1)  # Position the logo using place

        # Create a frame for buttons
        button_frame = ttk.Frame(self.master, style="TFrame")
        button_frame.place(relx=0.02, rely=0.80, anchor='w')  # Adjusted rely value to position below the logo

        # Create buttons for previous scan report and log review
        btn_prev_report = ttk.Button(button_frame, text="See Previous Scan Report", command=self.show_prev_report)
        btn_review_log = ttk.Button(button_frame, text="Review Log", command=self.review_log)

        # Position the buttons within the frame using grid
        btn_prev_report.grid(row=1, column=0, padx=5, pady=10)
        btn_review_log.grid(row=1, column=1, padx=5, pady=10)

    def show_prev_report(self):
        messagebox.showinfo("Previous Scan Report", "Displaying previous scan report...")

    def review_log(self):
        messagebox.showinfo("Review Log", "Opening log review...")

    def full_scan(self):
        self.scanning = True
        messagebox.showinfo("Full Scan", "Performing full system scan...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Full system scan was aborted.")
                return
            time.sleep(1)  # Simulate work being done
        self.scanning = False

    def file_scan(self):
        self.scanning = True
        messagebox.showinfo("File Scan", "Scanning file system for changes...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "File system scan was aborted.")
                return
            time.sleep(1)
        self.scanning = False

    def registry_scan(self):
        self.scanning = True
        messagebox.showinfo("Registry Scan", "Monitoring Windows registry changes...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Registry monitoring was aborted.")
                return
            time.sleep(1)
        self.scanning = False

    def network_scan(self):
        self.scanning = True
        messagebox.showinfo("Network Scan", "Analyzing network connections and ports...")
        for i in range(5):
            if not self.scanning:
                messagebox.show.info("Scan Aborted", "Network analysis was aborted.")
                return
            time.sleep(1)
        self.scanning = False

    def process_scan(self):
        self.scanning = True
        messagebox.showinfo("Process Scan", "Checking running processes...")
        for i in range(5):
            if not self.scanning:
                messagebox.showinfo("Scan Aborted", "Process check was aborted.")
                return
            time.sleep(1)
        self.scanning = False

    def stop_scan(self):
        self.scanning = False

# root = tk.Tk()
# app = HIDSApp(root)
# root.mainloop()