import tkinter as tk
from tkinter import messagebox

def show_alert(message):
    # Create a new Tkinter window for the alert
    alert_window = tk.Tk()
    alert_window.withdraw()  # Hide the main window
    messagebox.showinfo("Alert", message)  # Show the alert with the message
    alert_window.destroy()  # Destroy the alert window after the message is shown