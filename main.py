import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
from tkinter import messagebox
import sys
import time
import speech_recognition as sr
import pyttsx3
import pyautogui
import requests
from MobileTouchPad import get_local_ip
import signal
import psutil
import threading

# Define global variables
subprocess_instance = None
stop_window = None
open_controller_button = None
learn_about_button = None

def takeCommand():
    global mic_button
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.8
        r.energy_threshold = 400
        r.non_speaking_duration = 0.02
        r.adjust_for_ambient_noise(source, duration=0.1)

        try:
            audio = r.listen(source, timeout=8.0)
            print('Recognizing..')
            text = r.recognize_google(audio, language='en-in')
            print(f'User said: {text}\n')
            return text

        except sr.WaitTimeoutError:
            print('Listening timed out. Please try again.')
            mic_button.config(state='normal')  # Enable the mic_button in case of timeout
            return None

        except Exception as e:
            print(e)
            print('Say that again please...')
            mic_button.config(state='normal')  # Enable the mic_button in case of exception
            return None

def enable_mic_button():
    mic_button.config(state='normal')

command_in_progress = False

def on_mic_click():
    global command_in_progress

    # Check if a command is already in progress, if yes, return without doing anything
    if command_in_progress:
        return

    # Set the flag to indicate command execution is in progress
    command_in_progress = True

    mic_button.config(state='disabled')  # Disable the mic_button
    
    text = takeCommand()
    if text:
        pyautogui.typewrite(text)

    # Reset the flag and enable the mic_button after a short delay
    mic_button.after(700, reset_button_state)

def reset_button_state():
    global command_in_progress
    command_in_progress = False
    mic_button.config(state='normal')  # Enable the mic_button

def create_stop_window():
    global stop_window
    global mic_button
    stop_window = tk.Toplevel()
    stop_window.title("Stop Controller")
    stop_window.geometry("35x70")
    stop_window.config(bg="white")  # Set background color of the window to black
    stop_window.overrideredirect(True)
    stop_window.attributes('-alpha', 0.8)  # Set transparency level of the window (optional)
    stop_window.wait_visibility()  # Wait for the window to be visible before withdrawing it
    stop_window.withdraw()

    # Add this section to load the 2 image files
    stop_img = tk.PhotoImage(file=os.path.join(base_path,"./images/stop.png"))
    mic_img = tk.PhotoImage(file=os.path.join(base_path,"./images/mic.png"))

    button_frame = tk.Frame(stop_window, bg="white")
    button_frame.pack(fill=tk.BOTH, expand=True)

    stop_button = tk.Button(button_frame, image=stop_img, borderwidth=0, highlightthickness=0, bg="white", activebackground="white", command=stop_subprocess)
    stop_button.stop_img = stop_img
    stop_button.pack(fill=tk.X)

    global mic_button  # Declare mic_button as global
    mic_button = tk.Button(button_frame, image=mic_img, borderwidth=0, highlightthickness=0, bg="white", activebackground="white", command=on_mic_click)
    mic_button.stop_img = mic_img
    mic_button.pack(fill=tk.X, pady=(2, 0))

    stop_window.attributes('-topmost', True)

def mobile_stop_window():
    global stop_window
    stop_window = tk.Toplevel()
    stop_window.title("Stop Controller")
    stop_window.geometry("50x80")  # Set the size of the window
    stop_window.config(bg="white")  # Set background color of the window to white
    stop_window.overrideredirect(True)  # Remove window decorations
    stop_window.attributes('-alpha', 0.8)  # Set transparency level of the window (optional)
    stop_window.wait_visibility()  # Wait for the window to be visible before withdrawing it
    stop_window.withdraw()

    stopm_img = tk.PhotoImage(file=os.path.join(base_path,"./images/stopm.png"))
    mic_img= tk.PhotoImage(file=os.path.join(base_path,"./images/mic.png"))

    button_frame = tk.Frame(stop_window, bg="white")
    button_frame.pack(fill=tk.BOTH, expand=True)

    stop_button = tk.Button(button_frame, image=stopm_img, borderwidth=0, highlightthickness=0, bg="white", activebackground="white", command=stop_subprocess)
    stop_button.stop_img = stopm_img
    stop_button.pack(pady=4)

    global mic_button  # Declare mic_button as global
    
    mic_button = tk.Button(button_frame,image=mic_img, borderwidth=0, highlightthickness=0, bg="white", activebackground="white", command=on_mic_click)
    mic_button.stop_img = mic_img
    mic_button.pack(fill=tk.X, pady=5)
    stop_window.attributes('-topmost', 'true')
    stop_window.protocol("WM_DELETE_WINDOW", lambda: stop_subprocess())

def stop_subprocess():
    global subprocess_instance
    global open_controller_button
    global mobile_button
    global stop_window

      # Disable the mobile button
    """"
    local_ip = get_local_ip()
    response = requests.get(f'http://{local_ip}:48080/disconnect')
    if response.status_code == 200:
        print('Socket connection disconnected successfully')
    else:
        print('Socket connection disconnected successfully')
"""
    if subprocess_instance:
        # Get the subprocess PID
        pid = subprocess_instance.pid

        try:
            # Terminate the process and all its children
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
            
            subprocess_instance.wait(timeout=0.5)  # Wait for the process to terminate
            
        except psutil.NoSuchProcess:
            pass

        subprocess_instance = None
        if stop_window:
            stop_window.destroy()
        if open_controller_button:
            open_controller_button.config(state=tk.NORMAL)
        if mobile_button:
            mobile_button.config(state=tk.NORMAL)
        welcome_window.state('normal')

def minimize_window():
    welcome_window.iconify()

def on_stop_window_close():
    stop_subprocess()
    welcome_window.destroy()


def monitor_terminal_output():
    # This function will run in a separate thread to monitor the terminal output
    import subprocess
    
    process = subprocess.Popen(["python", "Virtual_Controller.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    while True:
        output_line = process.stdout.readline()
        if "INFO: Created TensorFlow Lite XNNPACK delegate for CPU" in output_line:
            # Close the popup when the desired message is found
            popup.destroy()
            break

def open_controller():
    global subprocess_instance
    global stop_window
    global open_controller_button
    global popup

    if subprocess_instance is None:
        subprocess_instance = subprocess.Popen(["python", "Virtual_Controller.py"])
        threading.Thread(target=monitor_terminal_output).start()
        create_stop_window()
        open_controller_button.config(state=tk.DISABLED)
        stop_window.deiconify()
        minimize_window()
        
        # Display a popup message indicating that the controller is starting
        popup = tk.Toplevel(welcome_window)
        popup.overrideredirect(True)
        popup_width = 330
        popup_height = 80
        screen_width = welcome_window.winfo_screenwidth()
        screen_height = welcome_window.winfo_screenheight()
        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.configure(bg='#101010')
        label = tk.Label(popup, text="Controller is Starting..Please Wait!", font=("Helvetica", 12),fg='#00FF00', bg='#101010')
        label.pack(pady=20)

def open_mobile():
    global subprocess_instance
    global mobile_button

    if subprocess_instance is None:
        subprocess_instance = subprocess.Popen(["python", "MobileTouchpad.py"])
        
        mobile_stop_window()  # Create the stop window
        stop_window.deiconify()  # Show the stop window
        minimize_window()  # Minimize the main window

        mobile_button.config(state=tk.DISABLED)  # Disable the mobile button


def Learn_about():
    global subprocess_instance

    if subprocess_instance is None:
        fade_out(welcome_window)
        subprocess_instance = subprocess.Popen(["python", "Learn_About.py"])


def fade_out(window, alpha=1.0):
    """
    Fade out the given window.
    """
    if alpha > 0:
        alpha -= 0.1  # Adjust the fade speed by changing the decrement value
        window.attributes('-alpha', alpha)
        window.after(50, lambda: fade_out(window, alpha))
    else:
        window.withdraw()  # Hide the window once it's fully faded out
        

def close_window():
    global welcome_window
    confirm_exit = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit Desktop Controller?")
    if confirm_exit:
        welcome_window.destroy()

def on_enter_open(event):
    open_controller_button.config(bg="#00FF00", fg="black")
    learn_about_button.config(state=tk.DISABLED)  # Disable Learn About button hover effect
    mobile_button.config(state=tk.DISABLED)

def on_leave_open(event):
    open_controller_button.config(bg=neon_bg, fg=neon_fg)
    learn_about_button.config(state=tk.NORMAL)  # Enable Learn About button hover effect
    mobile_button.config(state=tk.NORMAL)

def on_enter_mobile(event):
    mobile_button.config(bg="#00FF00", fg="black")
    open_controller_button.config(state=tk.DISABLED) 
    learn_about_button.config(state=tk.DISABLED)

def on_leave_mobile(event):
    mobile_button.config(bg=neon_bg, fg=neon_fg)
    open_controller_button.config(state=tk.NORMAL) 
    learn_about_button.config(state=tk.NORMAL)

def on_enter_learn(event):
    learn_about_button.config(bg="#00FF00", fg="black")
    open_controller_button.config(state=tk.DISABLED)  # Disable Open Controller button hover effect
    mobile_button.config(state=tk.DISABLED)

def on_leave_learn(event):
    learn_about_button.config(bg=neon_bg, fg=neon_fg)
    open_controller_button.config(state=tk.NORMAL)  # Enable Open Controller button hover effect
    mobile_button.config(state=tk.NORMAL)

def center_content(event=None):
    screen_width = welcome_window.winfo_screenwidth()
    screen_height = welcome_window.winfo_screenheight()
    window_width = welcome_window.winfo_width()
    window_height = welcome_window.winfo_height()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    welcome_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create the main window
welcome_window = tk.Tk()
welcome_window.title("Desktop Controller")
welcome_window.configure(bg='#101010')

# Use base_path to construct paths to files
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Define image paths
icon_path = os.path.join(base_path, "./images/favicon.png")
logo_path = os.path.join(base_path, "./images/logo.gif")

# Set default values for colors
neon_fg = "#00FF00"
neon_bg = "#101010"

# Load the favicon
try:
    con_image = tk.PhotoImage(file=icon_path)
    welcome_window.iconphoto(True, con_image)
except FileNotFoundError:
    print("Error: favicon.ico file not found! Using default icon.")

# Set window state
welcome_window.state('zoomed')

# Load the logo image
try:
    if not os.path.exists(logo_path):
        raise FileNotFoundError
    logo_image = Image.open(logo_path)
    
    # Resize the logo image
    desired_width = 300
    desired_height = 300
    logo_image = logo_image.resize((desired_width, desired_height), Image.LANCZOS)
    
    logo_image = ImageTk.PhotoImage(logo_image)
except FileNotFoundError:
    print("Error: logo.gif file not found! Using default image.")

# Create labels and buttons
introduction_label = tk.Label(welcome_window, text="Welcome to Desktop Controller!", font=("Helvetica", 24, "bold"), fg=neon_fg, bg=neon_bg)
introduction_label.pack(pady=(100, 10))

information_label = tk.Label(welcome_window, text="This application allows you to control your desktop virtually.", font=("Helvetica", 18), fg=neon_fg, bg=neon_bg)
information_label.pack(pady=(0, 20))

# Use default image if logo_image is not found
if 'logo_image' not in locals():
    logo_image = tk.PhotoImage(file="./images/logo.gif")  # Provide the path to your default logo image here

logo_label = tk.Label(welcome_window, image=logo_image, bg=neon_bg)
logo_label.pack(pady=10)

open_controller_button = tk.Button(welcome_window, text="Open Controller", command=open_controller, font=("Helvetica",14, "bold"), fg=neon_fg, bg=neon_bg, relief=tk.FLAT)
open_controller_button.pack(pady=(30, 10))

open_controller_button.bind("<Enter>", on_enter_open)
open_controller_button.bind("<Leave>", on_leave_open)

mobile_button = tk.Button(welcome_window, text="Mobile Controller", command=open_mobile, font=("Helvetica",14, "bold"), fg=neon_fg, bg=neon_bg, relief=tk.FLAT)
mobile_button.pack(pady=(10, 10))

mobile_button.bind("<Enter>", on_enter_mobile)
mobile_button.bind("<Leave>", on_leave_mobile)

learn_about_button = tk.Button(welcome_window, text="Learn About",command=Learn_about, font=("Helvetica", 14, "bold"), fg=neon_fg, bg=neon_bg, relief=tk.FLAT)
learn_about_button.pack(pady=(10,30))

learn_about_button.bind("<Enter>", on_enter_learn)
learn_about_button.bind("<Leave>", on_leave_learn)

welcome_window.bind("<Configure>", center_content)

# Bind the close_window() function to the window closing event
welcome_window.protocol("WM_DELETE_WINDOW", close_window)

welcome_window.mainloop()
