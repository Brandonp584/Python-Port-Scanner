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
                output = f"[OPEN] port {port} ({service})"
            else:
                output = f"[OPEN] port {port} (Unknown)"


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