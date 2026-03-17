import socket 

target = "127.0.0.1"

def port_scan(target, port):
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

        else:
            print(f"[CLOSED] Port {port}")
        
        # 5. Close the connection
        s.close()

    except Exception as e:
        print(f"An error occurred while scanning port {port}: {e}")

# Scan ports 1-1024
for port in range(1, 1025):
    port_scan(target, port)