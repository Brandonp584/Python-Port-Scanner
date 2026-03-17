import socket 
from threading import Thread

target = "127.0.0.1"

def port_scan( port):
    try:
        # 1. Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Set a timeout for the connection attempt
        s.settimeout(2)

        # 3. Attempt to connect
        result = s.connect_ex((target, port))

        # 4. Check the result
        if result == 0:
            print(f"[OPEN] Port {port}")
        
        # 5. Close the connection
        s.close()

    except Exception as e:
        print(f"An error occurred while scanning port {port}: {e}")

threads = []
# Scan ports from 1 to 6000
for port in range(1, 6000):
    t = Thread(target=port_scan, args=(port,))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print(f"Scanning port {port}")