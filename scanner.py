import socket 
from concurrent.futures import ThreadPoolExecutor

target = "127.0.0.1"

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
            print(f"[OPEN] Port {port}")
        
        # 5. Close the connection
        s.close()

    except Exception as e:
        print(f"An error occurred while scanning port {port}: {e}")

print("Starting scan...")

# Scan ports from 1 to 6000
ports = range(1, 6000)

# Limit Threads
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(port_scan, ports)

print("Scan completed.")