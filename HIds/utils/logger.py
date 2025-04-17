import tkinter as tk
from tkinter import messagebox

def menu_command(menu_name):
    messagebox.showinfo("Menu Command", f"You selected {menu_name}")

# Create the main window
root = tk.Tk()
root.title("Tkinter Menu Example")
root.geometry("400x300")



# Configure the menu bar
root.config(menu=menu_bar)

# Start the main loop
root.mainloop()