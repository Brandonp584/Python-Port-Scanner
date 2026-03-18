# 🔎 Python Port Scanner (Localhost)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/status-active-success)
![Made With](https://img.shields.io/badge/Made%20with-Python-blue)

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Brandonp584/Python-Port-Scanner.git

cd YOUR_REPO_NAME
```

### 2. Ensure Python is installed
This Project requires:
```bash
Python 3.x
```

Check your version:
```bash
python --version
```

### 3. Install dependencies
```bash
pip install colorama
```

## 🚀 Quick Start

Run the scanner with default settings:
```bash
python scanner.py
```
Or run a custom scan:
```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000
```
## ✨ Features

### - ⚡ Fast Multi-threaded Scanning
    Scan thousands of ports quickly using ThreadPoolExecutor

### - 🔍 Smart Service Detection
    Identifies common services like HTTP, SSH, FTP, SMB, and more

### -  🛰️ Banner Grabbing
    Attempts to detect running services by analyzing responses

### -  🎯 Custom Port Scanning (CLI)
    Easily define target IP and port ranges from command line

### -  🖥️ Clean Output + Colored Output
    Displays only ports with readable service information with colored highlighting

### - 💾 File Output Support
    Optionally save results to a file

### -  🔒 Safe by Design
    Defaults to localhost (127.0.0.1) for secure testing

## 📌 Overview

This is a Python-based port scanner that identifies open ports on your local machine (127.0.0.1).

It includes:

⚡ Multi-threaded scanning for speed
🔍 Basic service detection (smart port mapping)
🛰️ Banner grabbing for identifying services

Built for learning, experimentation, and safe local testing.

## ⚡ Command-Line Interface (CLI)

You can now run scans without modifying the code.

### 🧪 Usage
```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000 --threads 100 --output results.txt 
```
### 🧩 Options
- --target → Target IP (default: 127.0.0.1)
- --start → Start port (default: 1)
- --end → End port (default: 6000)
- --threads → Number of Threads (100)
- --output → Save results to a file (None)

## 📌 Examples
### Default scan
```bash
python scanner.py
```
### Custom port range
```bash
python scanner.py --target 127.0.0.1 --start 20 --end 100
```
### High-speed scan
```bash
python scanner.py --threads 200
```
### Save results
```bash
python scanner.py --output results.txt
```
## 🧠 How It Works

### 1. Importing Modules
```python
import socket
from concurrent.futures import ThreadPoolExecutor
```
- socket → Handles network communication
- ThreadPoolExecutor → Enables fast multi-threading

### 2. Setting the Target
```python
target = "127.0.0.1"
```
- 127.0.0.1 = localhost
- Ensures safe and controlled testing

### 3. Common Port Mapping
```python
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
```
- Helps quickly identify known services
- Improves scan readability

### 4. Banner Grabbing
```python
def grab_banner(s, port):
```
- Attempts to interact with services
- Uses different techniques based on port:
- HTTP → Sends request
- FTP/SSH → Reads response

### 5. Creating the Scanner Function
```python
def port_scan(port):
```
- Connects to a port
- Detects if it's open
- Identifies the service

### 6. Socket Creation
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
- AF_INET → IPv4
- SOCK_STREAM → TCP

### 7. Timeout Control
```python
s.settimeout(1)
```
- Prevents long delays
- Keeps scans fast

### 8. Port Connection
```python
result = s.connect_ex((target, port))
```
- 0 → Open port
- Non-zero → Closed / filtered

### 9. Smart Detection Logic
- Uses:
- Port mapping
- Banner grabbing
- Example output:
```bash
[OPEN] Port 22 (SSH - ssh-2.0-openssh...)
[OPEN] Port 80 (HTTP)
[OPEN] Port 5501 (Live Server - http)
```
## 10. Multi-threaded Scanning
```python
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(port_scan, ports)
```
- Scans many ports at the same time
- Much faster than single-threaded scanning

## 💻 Full Code
```python
import socket 
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Argyment Parser
parser = argparse.ArgumentParser(description="Python Port Scanner")

parser.add_argument("--target", type=str, default="127.0.0.1", help="Target IP address")
parser.add_argument("--start", type=int, default=1, help="Start port")
parser.add_argument("--end", type=int, default=6000, help="End port")
parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads")
parser.add_argument("--output", type=str, help="Optional: save results to a file")

args = parser.parse_args()

target = args.target
ports = range(args.start, args.end + 1)

# Common ports and their services
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

# Banner Grabbing
def grab_banner(s, port):
    try:
        # HTTP Ports
        if port in [80, 8080, 5501]:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode().lower()
            if "http" in banner:
                return "HTTP"
        
        # FTP / SSH Banners
        elif port in [21, 22]:
            banner = s.recv(1024).decode().lower()
            return banner.strip()
        
        return "Unknown"
    
    except:
        return "Unknown"        

# Port Scanner
def port_scan( port):
    try:
        # 1. Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Set a timeout for the connection attempt
        s.settimeout(1)

        # 3. Attempt to connect
        result = s.connect_ex((target, port))

        # 4. Check the result
        if result == 0:
            service = common_ports.get(port, "")
            banner = grab_banner(s, port)

            if banner != "Unknown":
                output = f"[OPEN] Port  {port} ({service}) - Banner: {banner}"
            elif service:
                output = f"[OPEN] Port {port} ({service})"
            else:
                output = f"[OPEN] Port {port} (Unknown)"


            # Print coloured output
            print(Fore.GREEN + output + Style.RESET_ALL)

            # Optional: Save results to a file
            if args.output:
                with open(args.output, "a") as f:
                    f.write(output + "\n")
        
        # 5. Close the connection
        s.close()

    except Exception as e:
        print(Fore.RED + f"Error scanning port {port}: {e}" + Style.RESET_ALL)

# Run Scan
print(Fore.CYAN + f"Starting scan on {target} with ports {args.start}-{args.end} using {args.threads} threads..." + Style.RESET_ALL)

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    executor.map(port_scan, ports)

print(Fore.CYAN + "Scan Complete." + Style.RESET_ALL)
```

## 📊 Output Behavior
- Displays only open ports
- Port number
- Service name
- Optional banner info
- Fast execution with threading

## 🔒 Safety Notice
Use only on:
- ✅ Localhost (127.0.0.1)
- ✅ Personal learning environments

## ⚠️ Do NOT scan:
- ❌ External servers
- ❌ Networks you don’t own
- ❌ Systems without permission

## 🚀 Future Improvements

- Multi-threading (Implemented)
- ThreadPoolExecutor (Better performance) - Implemented
- Banner grabbing (identify services) - Implemented
- Command-line arguments - Implemented
- Scanning different IP addresses - Implemented
- Service detection (HTTP, FTP, etc.) - Implemented

## 📌 Author Notes

This project was built as part of learning:

- Networking fundamentals
- Python socket programming
- Multi-threading
- Basic cybersecurity concepts