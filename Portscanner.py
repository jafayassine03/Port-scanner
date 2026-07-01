import socket
import threading
import json
from queue import Queue
from datetime import datetime
import time

print("=" * 50)
print("Advanced Python Port Scanner")
print("=" * 50)

target = input("Enter IP address or hostname: ")

try:
    ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid hostname.")
    exit()

start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

total_ports = end_port - start_port + 1

print(f"\nTarget : {target}")
print(f"IP     : {ip}")
print(f"Scanning {total_ports} ports...\n")

common_ports = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt"
}

queue = Queue()
lock = threading.Lock()

open_ports = []
scanned = 0

start_time = time.time()


def scan(port):
    global scanned

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        result = s.connect_ex((ip, port))

        with lock:
            scanned += 1
            print(f"\rProgress: {scanned}/{total_ports}", end="")

        if result == 0:
            service = common_ports.get(port, "Unknown")
            with lock:
                open_ports.append({
                    "port": port,
                    "service": service
                })
                print(f"\n[OPEN] {port:<5} {service}")

    except:
        pass

    finally:
        s.close()


def worker():
    while True:
        port = queue.get()
        scan(port)
        queue.task_done()


for _ in range(100):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

for port in range(start_port, end_port + 1):
    queue.put(port)

queue.join()

elapsed = round(time.time() - start_time, 2)

print("\n")
print("=" * 50)
print("Scan Complete")
print("=" * 50)

print(f"Target        : {target}")
print(f"IP Address    : {ip}")
print(f"Ports Scanned : {total_ports}")
print(f"Open Ports    : {len(open_ports)}")
print(f"Time Taken    : {elapsed} seconds")

with open("scan_results.txt", "w") as f:
    f.write(f"Target: {target}\n")
    f.write(f"IP: {ip}\n")
    f.write(f"Date: {datetime.now()}\n\n")

    for port in open_ports:
        f.write(f"{port['port']} - {port['service']}\n")

with open("scan_results.json", "w") as f:
    json.dump({
        "target": target,
        "ip": ip,
        "scan_date": str(datetime.now()),
        "ports_scanned": total_ports,
        "time_taken": elapsed,
        "open_ports": open_ports
    }, f, indent=4)

print("\nResults saved:")
print(" - scan_results.txt")
print(" - scan_results.json")