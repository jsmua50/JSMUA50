# Remote Access Tool

A simple and secure remote access tool designed for IT support and system administration. This tool allows users to remotely control, manage systems, and perform various actions, including file transfer, screen sharing, and executing commands. It supports both client and server modes.

## Features

- **Secure connection**: Encryption to ensure secure communications.
- **File transfer**: Easily send files between the client and server.
- **Command execution**: Execute shell commands remotely on the target machine.
- **Screen sharing**: View the screen of the target machine.
- **Cross-platform**: Works on both Windows and Linux machines.

## Requirements

- **Python 3.x** (Make sure Python is installed on both client and server machines).
- The following libraries are required. These can be installed using `pip` from the `requirements.txt`:

  - `requests`
  - `pyautogui`
  - `pycryptodome`
  - `psutil`
