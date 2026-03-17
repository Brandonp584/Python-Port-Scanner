🔎 Python Port Scanner (Localhost)

This is a simple Python-based port scanner that checks which ports are open on your own machine (127.0.0.1). It is designed for leraning purposes and safe testing.

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
    "def port_scan(target, port):"

- This function checks a single port.
- It takes:
    - target (IP address)
    - port (port number)

4. Using try/expect (error handling)
    "try"

- Prevents the program from crashing if something goes wrong.

    "expect socket.error as e:"

- Catches network-related errors.
- Prints the error instead of stopping the program.

5. Creating a socket 
    "s= socket.socket(socket.AF_inet, socket.SOCK_STREAM)"

- AF_INET → IPv4
- SOCK_STREAM → TCP Connection

6. Setting a timeout
    "s.settimeout(2)"

- Waits up to 2 seconds per port.
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

10. Scanning multiple ports
    "for port in range(1, 1025):"

- Loops through ports 1-1024
- These are known as well-known ports

🚀 Future Improvements

- Multi-threading (faster scans)
- Banner grabbing (idenify services)
- Command-line arguments
- Scanning different IPs