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
