# Python Port Scanner

A fast and lightweight multithreaded port scanner built with Python. This project scans a target host for open TCP ports and identifies common services running on those ports.

## Features

* Multithreaded scanning for improved speed
* Supports scanning a custom range of TCP ports
* Resolves hostnames to IP addresses
* Identifies common services (HTTP, HTTPS, SSH, FTP, etc.)
* Saves scan results to a text file
* Simple command-line interface
* Built using only Python's standard library

## Requirements

* Python 3.8 or newer

No external libraries are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/python-port-scanner.git
cd python-port-scanner
```

## Usage

Run the scanner:

```bash
python port_scanner.py
```

Example:

```text
Enter IP address or hostname: scanme.nmap.org
Start Port: 1
End Port: 1000
```

The scanner will display all detected open ports and save the results to `scan_results.txt`.

## How It Works

1. Resolves the target hostname to an IP address.
2. Creates a pool of worker threads.
3. Attempts to connect to each port in the specified range.
4. Reports any open ports and their common services.
5. Saves the results to a text file.

## Example Output

```text
==================================================
Simple Python Port Scanner
==================================================

Scanning 192.168.1.1...

[OPEN] 22    SSH
[OPEN] 80    HTTP
[OPEN] 443   HTTPS

==================================================
Scan Complete
==================================================
```

## Educational Purpose

This project is intended for learning Python networking, sockets, threading, and basic cybersecurity concepts.

**Only scan systems that you own or have explicit permission to test. Unauthorized scanning may violate laws or organizational policies.**

## Future Improvements

* Banner grabbing
* Progress bar
* Export to JSON or CSV
* Colorized terminal output
* Scan history
* IPv6 support
* UDP port scanning
* Service version detection
