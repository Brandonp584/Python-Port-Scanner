🔎 Python Port Scanner (Localhost)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/status-active-success)
![Made With](https://img.shields.io/badge/Made%20with-Python-blue)

This is a simple Python-based port scanner that checks which ports are open on your own machine (127.0.0.1). It is designed for learning purposes and safe testing.

🧠 How It Works

1. Importing the socket module
    "import socket"

- This allows Python to create network connections.
- Sockets are used to communicate with other devices or       services.

2. Setting the target
    "target = "127.0.0.1"

- 127.0.0.1 means your own computer (localhost).
- This ensures all scans stay on your machine.

3. Creating the function
    "def port_scan(port):"

- This function checks a single port.
- It takes
    - port (port number)

4. Using try/except (error handling)
    "try"

- Prevents the program from crashing if something goes wrong.

    "except Exception as e:"

- Catches network-related errors.
- Prints the error instead of stopping the program.

5. Creating a socket 
    "s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)"

- AF_INET → IPv4
- SOCK_STREAM → TCP Connection

6. Setting a timeout
    "s.settimeout(1)"

- Waits up to 1 seconds per port.
- Prevents the scan from hanging too long.

7. Connecting to the port
    "result = s.connect_ex((target, port))"

- Attempts a connection to the port.
- Returns:
    - 0 → success (port is open)
    - non-zero → failed (Closed or filtered)

8. Checking if the port is open
    "if result == 0:"

- If true → port is open
- Otherwise → closed

9. Closing the socket
    "s.close()"

- Always close connections to free resources.

10. Scanning multiple ports with threading
    "for port in range(1, 6000):"

- Scans ports 1-6000

    "Thread(target=port_scan, args=(port,))

- Uses threading for faster scanning
- Multiple ports are scanned at the same time

📊 Output Behavor

- Only open ports are displayed
- Progress updates appear during scanning
- A final message confirms completion

Example Output

Starting scan...
[OPEN] Port 135
[OPEN] Port 445
[OPEN] Port 5501
Scan complete.

🔒 Safety Notice

This tool is intened for:

- Localhost (127.0.0.1)
- Personal learning environments

⚠️ DO NOT SCAN:

- External servers
- Networks you dont own
- Systems without permission

🚀 Future Improvements

- Multi-threading (Implemented)
- ThreadPoolExecutor (Better performance)
- Banner grabbing (idenify services)
- Command-line arguments
- Scanning different IP addresses
- Service detection (HTTP, FTP, etc.)

📌 Author Notes

This project was built as part of learning:

- Networking fundamentals
- Python socket programming
- Basic cybersecurity concepts