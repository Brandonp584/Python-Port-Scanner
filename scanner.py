import socket 
import argparse
import sys
import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Argument Parser
parser = argparse.ArgumentParser(description="Python Port Scanner")

parser.add_argument("--target", type=str, default="127.0.0.1", help="Target IP address")
parser.add_argument("--start", type=int, default=1, help="Start port")
parser.add_argument("--end", type=int, default=6000, help="End port")
parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads")
parser.add_argument("--output", type=str, help="Optional: save results to a file")
parser.add_argument("--mode", choices=["fast", "full"], default="fast", help="Scan mode")
args = parser.parse_args()

target = args.target

# Mode Logic
if args.mode == "fast":
    ports = [p for p in range(args.start, args.end + 1) if p <= 1000]
    timeout_value = 0.5
else:
    ports = range(args.start, args.end + 1)
    timeout_value = 1

# Common ports and their services
common_ports = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    135: "RPC",
    3000: "React / Node",
    5000: "Flask",
    5173: "Vite",
    5432: "PostgreSQL",
    5501: "Live Server",
    6379: "Redis",
    8080: "HTTP-Alt",
    27017: "MongoDB"    
}

open_ports = []

# Progress Tracking
progress_lock = Lock()
total_ports = len(ports)
completed_ports = 0
progress_color = Fore.CYAN

# Scan Speed
start_time = time.time()

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
    global completed_ports

    try:
        # 1. Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Set a timeout for the connection attempt
        s.settimeout(timeout_value)

        # 3. Attempt to connect
        result = s.connect_ex((target, port))

        # 4. Check the result
        if result == 0:
            open_ports.append(port)
            service = common_ports.get(port, "")
            banner = grab_banner(s, port)

            if banner != "Unknown":
                output = f"[OPEN] Port {port} - Service: {banner}"
            elif service:
                output = f"[OPEN] Port {port} ({service})"
            else:
                output = f"[OPEN] Port {port} (Unknown Service)"

            # Print above progress bar
            with progress_lock:
                sys.stdout.write("\n")
                print(Fore.YELLOW + output + Style.RESET_ALL)
            
            # Optional: Save results to a file
            if args.output:
                with open(args.output, "a") as f:
                    f.write(f"Scan target: {target}\n")
                    f.write(f"Port range: {args.start}-{args.end}\n\n")
        
        # 5. Close the connection
        s.close()

    except:
        pass

    # Update Progress Bar
    with progress_lock:
        completed_ports += 1

        # Only Update every 50 ports to reduce flickering
        if completed_ports % 50 != 0 and completed_ports != total_ports:
            return
        
        elapsed_time = time.time() - start_time
        speed = completed_ports / elapsed_time if elapsed_time > 0 else 0

        #ETA Calculation (minutes + seconds)
        remaining_ports = total_ports - completed_ports
        eta = remaining_ports / speed if speed > 0 else 0

        eta_seconds = int(eta)
        minutes = eta_seconds // 60
        seconds = eta_seconds % 60
        eta_display = f"{minutes}m {seconds}s"

        percent = (completed_ports / total_ports) * 100
        bar_length = 40
        filled_length = int(bar_length * completed_ports // total_ports)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(
            f"\r{progress_color}[{bar}] {percent:.1f}% "
            f"({completed_ports}/{total_ports}) | {speed:.1f} ports/sec | Open: {len(open_ports)} | ETA: {eta_display}"
        )
        sys.stdout.flush()

# Run Scan
print(Fore.CYAN + f"Starting scan on {target} with ports {args.start}-{args.end} using {args.threads} threads..." + Style.RESET_ALL)

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    executor.map(port_scan, ports)

print() # Move to the next line after progress bar

print(Fore.CYAN + "\n==== Scan Summary ====" + Style.RESET_ALL)

if open_ports:
    sorted_ports = sorted(open_ports)
    print(Fore.MAGENTA + f"Open Ports: {', '.join(map(str, sorted_ports))}" + Style.RESET_ALL)
    print(Fore.MAGENTA + f"Total Open Ports: {len(sorted_ports)}" + Style.RESET_ALL)

else:
    print(Fore.YELLOW + "No open ports found." + Style.RESET_ALL)

print(Fore.CYAN + "Scan Completed." + Style.RESET_ALL)