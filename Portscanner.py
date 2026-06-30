import socket
import threading
from queue import Queue
from datetime import datetime

print("=" * 50)
print("Simple Python Port Scanner")
print("=" * 50)

target = input("Enter IP address or hostname: ")

try:
    target = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid hostname.")
    exit()

start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

print(f"\nScanning {target}...")
print(f"Started: {datetime.now()}\n")

queue = Queue()
open_ports = []
lock = threading.Lock()

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

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    result = s.connect_ex((target, port))

    if result == 0:
        service = common_ports.get(port, "Unknown")
        with lock:
            open_ports.append((port, service))
            print(f"[OPEN] {port:<5} {service}")

    s.close()

def worker():
    while True:
        port = queue.get()
        scan(port)
        queue.task_done()

for _ in range(100):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

for port in range(start_port, end_port + 1):
    queue.put(port)

queue.join()

print("\n" + "=" * 50)
print("Scan Complete")
print("=" * 50)

if open_ports:
    print("Open Ports:")
    for port, service in sorted(open_ports):
        print(f"{port:<5} {service}")

    with open("scan_results.txt", "w") as f:
        f.write(f"Target: {target}\n\n")
        for port, service in sorted(open_ports):
            f.write(f"{port:<5} {service}\n")

    print("\nResults saved to scan_results.txt")
else:
    print("No open ports found.")