import socket
import threading
import json
import subprocess
import platform
import re
import csv
from queue import Queue
from datetime import datetime
import time

def ping_target(ip):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", ip]
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except:
        return False

print("=" * 50)
print("Advanced Python Port Scanner")
print("=" * 50)

target = input("Enter IP address or hostname: ")

try:
    ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid hostname.")
    exit()

if not ping_target(ip):
    print("Target is unreachable via ping. Proceeding anyway...")

start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

total_ports = end_port - start_port + 1

print(f"\nTarget : {target}")
print(f"IP     : {ip}")
print(f"Scanning {total_ports} ports...\n")

common_ports = {
    20: "FTP Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt"
}

queue = Queue()
lock = threading.Lock()
open_ports = []
scanned = 0
start_time = time.time()

def detect_os():
    try:
        cmd = ["ping", "-n", "1", ip] if platform.system().lower() == "windows" else ["ping", "-c", "1", ip]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode(errors="ignore")
        match = re.search(r"TTL=(\d+)", output, re.IGNORECASE) or re.search(r"ttl=(\d+)", output)
        if match:
            ttl = int(match.group(1))
            if ttl <= 64: return f"Linux / Unix (TTL={ttl})"
            elif ttl <= 128: return f"Windows (TTL={ttl})"
            elif ttl <= 255: return f"Cisco / Network Device (TTL={ttl})"
        return "Unknown"
    except:
        return "Unknown"

def grab_banner(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        if port in [80, 8080]:
            s.send(b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner.replace("\r", "").replace("\n", " ")[:120] if banner else "Unavailable"
    except:
        return "Unavailable"

def scan(port):
    global scanned
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        if s.connect_ex((ip, port)) == 0:
            service = common_ports.get(port, "Unknown")
            banner = grab_banner(port)
            with lock:
                open_ports.append({"port": port, "service": service, "banner": banner})
                print(f"\n[OPEN] {port:<5} {service} | Banner: {banner}")
    finally:
        with lock:
            scanned += 1
            print(f"\rProgress: {scanned}/{total_ports}", end="")
        s.close()

def worker():
    while True:
        port = queue.get()
        scan(port)
        queue.task_done()

for _ in range(100):
    threading.Thread(target=worker, daemon=True).start()

for port in range(start_port, end_port + 1):
    queue.put(port)

queue.join()

elapsed = round(time.time() - start_time, 2)
os_guess = detect_os()

print("\n\n" + "=" * 50 + "\nScan Complete\n" + "=" * 50)
print(f"Target: {target} | IP: {ip} | OS: {os_guess}")
print(f"Time: {elapsed}s | Ports: {total_ports} | Open: {len(open_ports)}")

with open("scan_results.txt", "w") as f:
    f.write(f"Target: {target}\nIP: {ip}\nOS: {os_guess}\nDate: {datetime.now()}\n\n")
    for p in open_ports: f.write(f"{p['port']} - {p['service']}\nBanner: {p['banner']}\n\n")

with open("scan_results.json", "w") as f:
    json.dump({"target": target, "ip": ip, "os": os_guess, "open_ports": open_ports}, f, indent=4)

with open("scan_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Port", "Service", "Banner"])
    for p in open_ports: writer.writerow([p["port"], p["service"], p["banner"]])

with open("scan_summary.html", "w") as f:
    f.write(f"<html><body><h1>Scan Report for {target} ({ip})</h1><p>OS: {os_guess}</p><p>Time Taken: {elapsed}s</p><table border='1'><tr><th>Port</th><th>Service</th><th>Banner</th></tr>")
    for p in open_ports:
        f.write(f"<tr><td>{p['port']}</td><td>{p['service']}</td><td>{p['banner']}</td></tr>")
    f.write("</table></body></html>")

print("\nResults saved:")
print(" - scan_results.txt")
print(" - scan_results.json")
print(" - scan_results.csv")
print(" - scan_summary.html")

udp_scan = input("\nPerform UDP scan? (y/n): ").lower()
if udp_scan == 'y':
    print("UDP scan initiated...")
    udp_open = []
    udp_ports = []
    for p in range(start_port, min(end_port + 1, start_port + 100)):
        udp_ports.append(p)
    
    for port in udp_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        try:
            s.sendto(b"", (ip, port))
            s.recvfrom(1024)
            udp_open.append(port)
            print(f"[UDP OPEN] {port}")
        except socket.timeout:
            pass
        except:
            pass
        finally:
            s.close()
    
    with open("udp_scan_results.txt", "w") as f:
        f.write(f"UDP Scan Results for {target} ({ip})\nDate: {datetime.now()}\n\n")
        for port in udp_open:
            f.write(f"Port {port} - UDP Open\n")
    
    print(f"UDP scan complete. Found {len(udp_open)} open UDP ports.")

service_scan = input("\nPerform service version detection? (y/n): ").lower()
if service_scan == 'y' and open_ports:
    print("Detecting service versions...")
    for p in open_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, p['port']))
            s.send(b"HELP\r\n")
            response = s.recv(1024).decode(errors="ignore").strip()
            if response:
                p['version'] = response[:100]
            s.close()
        except:
            p['version'] = "Unavailable"
    
    with open("service_versions.json", "w") as f:
        json.dump({"target": target, "ip": ip, "services": open_ports}, f, indent=4)
    print("Service versions saved to service_versions.json")

trace_route = input("\nPerform traceroute? (y/n): ").lower()
if trace_route:
    print("Performing traceroute...")
    try:
        cmd = ["tracert", "-h", "30", ip] if platform.system().lower() == "windows" else ["traceroute", "-m", "30", ip]
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode(errors="ignore")
        with open("traceroute.txt", "w") as f:
            f.write(f"Traceroute to {target} ({ip})\n\n")
            f.write(result)
        print("Traceroute saved to traceroute.txt")
    except:
        print("Traceroute failed.")

stealth_mode = input("\nEnable stealth mode (slower scanning)? (y/n): ").lower()
if stealth_mode == 'y':
    print("Stealth mode enabled - scanning with random delays...")
    stealth_ports = []
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            if s.connect_ex((ip, port)) == 0:
                stealth_ports.append(port)
                print(f"[STEALTH OPEN] {port}")
        finally:
            s.close()
        time.sleep(0.1)
    
    with open("stealth_scan_results.txt", "w") as f:
        f.write(f"Stealth Scan Results for {target} ({ip})\n\n")
        for port in stealth_ports:
            f.write(f"Port {port} - Open\n")
    print(f"Stealth scan complete. Found {len(stealth_ports)} open ports.")

port_range_count = input("\nCount ports in custom range? (enter ports separated by commas): ")
if port_range_count:
    try:
        ports_list = [int(p.strip()) for p in port_range_count.split(",")]
        open_count = 0
        for port in ports_list:
            if any(p['port'] == port for p in open_ports):
                open_count += 1
        print(f"Found {open_count} open ports in specified range.")
    except:
        print("Invalid port list.")

ping_sweep = input("\nPerform local subnet ping sweep? (y/n): ").lower()
if ping_sweep == 'y':
    print("Initiating subnet ping sweep...")
    base_ip = ".".join(ip.split(".")[:3])
    active_hosts = []
    def sweep(host_ip):
        if ping_target(host_ip):
            with lock:
                active_hosts.append(host_ip)
                print(f"[ACTIVE] {host_ip}")
    sweep_threads = []
    for i in range(1, 255):
        h_ip = f"{base_ip}.{i}"
        t = threading.Thread(target=sweep, args=(h_ip,), daemon=True)
        sweep_threads.append(t)
        t.start()
    for t in sweep_threads:
        t.join()
    with open("ping_sweep_results.txt", "w") as f:
        f.write(f"Ping Sweep Results for Subnet {base_ip}.0/24\nDate: {datetime.now()}\n\n")
        for h in active_hosts:
            f.write(f"{h}\n")
    print(f"Ping sweep complete. Found {len(active_hosts)} active hosts.")

print("\nScan completed successfully!")
