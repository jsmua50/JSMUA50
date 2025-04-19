import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style
from ttkbootstrap.widgets import Checkbutton, Entry, Label, Button, Frame

# Initialize themed style
style = Style("cyborg")  # Options: flatly, superhero, darkly, solar, journal, etc.

# Main window setup
root = style.master
root.title("Mua Grabber Generator - by jsmua50")
root.geometry("750x750")
root.resizable(False, False)

# Variables
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

# --- Functions ---
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

    # Dummy placeholder code generation
    code = f"# Webhook: {webhook_url}\n# Features: {', '.join(selected_features)}"
    if image_path:
        code += f"\n# Image: {image_path}"

    code_output.delete(1.0, tk.END)
    code_output.insert(tk.END, code)

# --- UI Layout ---
main_frame = Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

Label(main_frame, text="Mua Grabber Builder", font=("Helvetica", 18, "bold")).pack(pady=(0, 10))
Label(main_frame, text="Enter Webhook URL:").pack(anchor="w")

webhook_entry = Entry(main_frame, width=50)
webhook_entry.pack(pady=(0, 10))

# Feature checkboxes
features_frame = Frame(main_frame)
features_frame.pack(pady=10)

for i, (name, var) in enumerate(selected_features_vars.items()):
    cb = Checkbutton(features_frame, text=name, variable=var, bootstyle="success-round-toggle")
    cb.grid(row=i//2, column=i % 2, sticky="w", padx=10, pady=5)

# Image select
Button(main_frame, text="Select Image", command=on_select_image_button_click, bootstyle="info").pack(pady=(15, 5))
image_label = Label(main_frame, text="No image selected", bootstyle="secondary")
image_label.pack()

# Build button
Button(main_frame, text="Build Code", command=on_build_button_click, bootstyle="success-outline").pack(pady=15)

# Output code
Label(main_frame, text="Generated Code Preview:").pack(anchor="w")
code_output = ScrolledText(main_frame, height=12, font=("Courier New", 10))
code_output.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()
