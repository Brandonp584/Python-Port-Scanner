🔎 Python Port Scanner (Localhost)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/status-active-success)
![Made With](https://img.shields.io/badge/Made%20with-Python-blue)

⚙️ Installation

1. Clone the repository
- git clone https://github.com/Brandonp584/Python-Port-Scanner.git
- cd YOUR_REPO_NAME

2. Ensure Python is installed
This Project requires:
- Python 3.x

Check your version:
- python --version

🚀 Quick Start
Run the scanner with default settings:
- python scanner.py

Or run a custom scan:
- python scanner.py --target 127.0.0.1 --start 1 --end 1000

✨ Features

- ⚡ Fast Multi-threaded Scanning
    Scan thousands of ports quickly using ThreadPoolExecutor

- 🔍 Smart Service Detection
    Identifies common services like HTTP, SSH, FTP, SMB, and more

-  🛰️ Banner Grabbing
    Attempts to detect running services by analyzing responses

-  🎯 Custom Port Scanning (CLI)
    Easily define target IP and port ranges from command line

-  🖥️ Clean Output
    Displays only ports with readable service information

-  🔒 Safe by Design
    Defaults to localhost (127.0.0.1) for secure testing

📌 Overview

This is a Python-based port scanner that identifies open ports on your local machine (127.0.0.1).

It includes:

⚡ Multi-threaded scanning for speed
🔍 Basic service detection (smart port mapping)
🛰️ Banner grabbing for identifying services

Built for learning, experimentation, and safe local testing.

⚡ Command-Line Interface (CLI)

You can now run scans without modifying the code.

🧪 Usage
python scanner.py --target 127.0.0.1 --start 1 --end 1000
🧩 Options

--target → Target IP (default: 127.0.0.1)

--start → Start port (default: 1)

--end → End port (default: 6000)

📌 Examples
# Default scan
python scanner.py

# Custom port range
python scanner.py --target 127.0.0.1 --start 20 --end 100

🧠 How It Works
1. Importing Modules
import socket
from concurrent.futures import ThreadPoolExecutor

socket → Handles network communication

ThreadPoolExecutor → Enables fast multi-threading

2. Setting the Target
target = "127.0.0.1"

127.0.0.1 = localhost (your own machine)

Ensures safe and controlled testing

3. Common Port Mapping
common_ports = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    135: "RPC",
    8080: "HTTP-Alt",
    5501: "Live Server"
}

Helps quickly identify known services

Improves scan readability

4. Banner Grabbing
def grab_banner(s, port):

Attempts to interact with services

Uses different techniques based on port:

HTTP → Sends request

FTP/SSH → Reads response

5. Creating the Scanner Function
def port_scan(port):

Connects to a port

Detects if it's open

Identifies the service

6. Socket Creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

AF_INET → IPv4

SOCK_STREAM → TCP

7. Timeout Control
s.settimeout(1)

Prevents long delays

Keeps scans fast

8. Port Connection
result = s.connect_ex((target, port))

0 → Open port

Non-zero → Closed / filtered

9. Smart Detection Logic

Uses:

Port mapping

Banner grabbing

Example output:

[OPEN] Port 22 (SSH - ssh-2.0-openssh...)
[OPEN] Port 80 (HTTP)
[OPEN] Port 5501 (Live Server - http)
10. Multi-threaded Scanning
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(port_scan, ports)

Scans many ports at the same time

Much faster than single-threaded scanning

💻 Full Code
import socket
from concurrent.futures import ThreadPoolExecutor

target = "127.0.0.1"

common_ports = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    135: "RPC",
    8080: "HTTP-Alt",
    5501: "Live Server"
}

def grab_banner(s, port):
    try:
        if port in [80, 8080, 5501]:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode().lower()
            if "http" in banner:
                return "HTTP"

        elif port in [21, 22]:
            banner = s.recv(1024).decode().lower()
            return banner.strip()

        return "Unknown"

    except:
        return "Unknown"


def port_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:
            service = common_ports.get(port, "")
            banner = grab_banner(s, port)

            if banner != "Unknown":
                print(f"[OPEN] Port {port} ({service} - {banner})")
            elif service:
                print(f"[OPEN] Port {port} ({service})")
            else:
                print(f"[OPEN] Port {port} (Unknown)")

        s.close()

    except Exception as e:
        print(f"Error on port {port}: {e}")


print("Starting scan...")

ports = range(1, 6000)

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(port_scan, ports)

print("Scan complete.")

📊 Output Behavior

Displays only open ports

Shows:

Port number

Service name

Optional banner info

Fast execution with threading

🔒 Safety Notice

This tool is intended for:

✅ Localhost (127.0.0.1)

✅ Personal learning environments

⚠️ Do NOT scan:

External servers

Networks you don’t own

Systems without permission

🚀 Future Improvements

- Multi-threading (Implemented)
- ThreadPoolExecutor (Better performance) - Implemented
- Banner grabbing (identify services) - Implemented
- Command-line arguments - Implemented
- Scanning different IP addresses
- Service detection (HTTP, FTP, etc.)

📌 Author Notes

This project was built as part of learning:

- Networking fundamentals
- Python socket programming
- Multi-threading
- Basic cybersecurity concepts