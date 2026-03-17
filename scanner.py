import socket 
import argparse
from concurrent.futures import ThreadPoolExecutor

# Argyment Parser
parser = argparse.ArgumentParser(description="Python Port Scanner")

parser.add_argument("--target", type=str, default="127.0.0.1", help="Target IP address")
parser.add_argument("--start", type=int, default=1, help="Start port")
parser.add_argument("--end", type=int, default=6000, help="End port")

args = parser.parse_args()

target = args.target
start_port = args.start
end_port = args.end

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
                print(f"[OPEN] Port {port} ({service}) - Banner: {banner}")
            elif service:
                print(f"[OPEN] Port {port} ({service})")
            else:
                print(f"[OPEN] Port {port} (Unknown)")
        
        # 5. Close the connection
        s.close()

    except Exception as e:
        print(f"An error occurred while scanning port {port}: {e}")

# Run Scan
print(f"Starting scan on {target}")

ports = range(start_port, end_port)

# Limit Threads
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(port_scan, ports)

print("Scan completed.")