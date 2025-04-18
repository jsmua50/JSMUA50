# Remote Access Tool

This project is a secure, cross-platform remote access tool that allows system administrators, IT professionals, and developers to manage and control remote machines efficiently. It enables various functionalities such as screen sharing, remote command execution, file transfer, and more. Whether you're providing IT support or managing remote systems, this tool streamlines the process and enhances productivity.

## Features

- **Secure Connections**: The tool uses encryption (SSL/TLS) to ensure a secure communication channel between client and server.
- **File Transfer**: Allows seamless file sharing between the client and server. You can send files to the remote system and receive files from it.
- **Remote Command Execution**: Remotely execute system commands, scripts, or programs on the target machine without having to physically access it.
- **Screen Sharing**: View the remote machine's screen, making it easier to monitor activities or help users troubleshoot issues in real time.
- **Cross-Platform**: Compatible with both Windows and Linux machines, enabling support for a variety of system environments.
- **Customizable Ports & IP Addresses**: The server and client can be configured to connect using specific IP addresses and ports.
- **Simple Command-Line Interface (CLI)**: Designed to be intuitive and straightforward, the tool can be operated from the command line with minimal configuration.
- **Multiple Session Support**: Allows the server to handle multiple incoming client connections simultaneously, making it useful for team-based operations.
- **Non-intrusive**: Operates in the background without interfering with the normal operations of the host machine, ensuring that system performance remains unaffected.

## Requirements

To run this tool, ensure that your environment meets the following requirements:

- **Python 3.x** (Python 3.6 or later)
- **Operating System**:
  - Windows (Windows 10/11 and older versions)
  - Linux (Ubuntu/Debian based systems recommended)
  - MacOS (experimental support)
- Required Python libraries are included in the `requirements.txt` file:
  - `requests`: For sending HTTP requests and interacting with the Discord webhook API.
  - `pyautogui`: Used for simulating mouse movements and keyboard inputs for screen sharing and remote control.
  - `pycryptodome`: For implementing encryption (SSL/TLS) to secure communication.
  - `psutil`: A library for accessing system and process information, including CPU and memory usage.
  - `socket`: For network communications between the client and server.
  - 
