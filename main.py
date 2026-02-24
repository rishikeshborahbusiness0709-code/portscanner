#!/usr/bin/env python3

import socket
import threading
import argparse
import json
import csv
import sys
import time
from queue import Queue
from datetime import datetime

# =====================================
# MATRIX INTRO (Clean Professional)
# =====================================
def matrix_intro():
    green = "\033[92m"
    reset = "\033[0m"

    print(green)
    print("Initializing Rishi Shadow Scanner...")
    for _ in range(3):
        print("010101010101010101010101010101010101010")
        time.sleep(0.2)
print("\033[92m")  # Green color start

print(r"""
██████╗ ██╗███████╗██╗  ██╗██╗    ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔══██╗██║██╔════╝██║  ██║██║    ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
██████╔╝██║███████╗███████║██║    ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
██╔══██╗██║╚════██║██╔══██║██║    ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
██║  ██║██║███████║██║  ██║██║    ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ 
                                                                                       
                        R I S H I   S H A D O W
""")

print("\033[0m")  # Reset color
    print(reset)


# =====================================
# COMMON SERVICE MAP
# =====================================
COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt"
}


# =====================================
# SCAN FUNCTION
# =====================================
def scan_port(ip, port, timeout, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))

        if result == 0:
            service = COMMON_SERVICES.get(port, "Unknown")

            banner = ""
            try:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                pass

            results.append({
                "port": port,
                "service": service,
                "banner": banner[:100]
            })

            print(f"[+] {port} OPEN ({service})")

        sock.close()
    except:
        pass


# =====================================
# THREAD WORKER
# =====================================
def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(args.target, port, args.timeout, results)
        queue.task_done()


# =====================================
# SAVE REPORTS
# =====================================
def save_reports(ip, results):

    # TXT
    with open(f"{ip}.txt", "w") as f:
        for r in results:
            f.write(f"{r['port']} - {r['service']}\n")

    # JSON
    with open(f"{ip}.json", "w") as f:
        json.dump(results, f, indent=4)

    # CSV
    with open(f"{ip}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["port", "service", "banner"])
        writer.writeheader()
        writer.writerows(results)

    print("\nReports saved as:")
    print(f"{ip}.txt | {ip}.json | {ip}.csv")


# =====================================
# BASIC VULNERABILITY HINTS
# =====================================
def basic_vuln_check(results):
    print("\nBasic Security Observations:")

    for r in results:
        if r["port"] == 21:
            print("⚠ FTP open — Check for anonymous login.")
        if r["port"] == 23:
            print("⚠ Telnet open — Insecure protocol.")
        if r["port"] == 80:
            print("ℹ HTTP open — Consider HTTPS.")


# =====================================
# MAIN
# =====================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Rishi Shadow Professional Port Scanner"
    )

    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range (example 20-80)")
    parser.add_argument("-t", "--timeout", type=float,
                        default=0.5, help="Timeout per port")

    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))

    matrix_intro()

    print(f"Scanning {args.target} from {start_port} to {end_port}\n")

    queue = Queue()
    results = []

    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(100):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    try:
        queue.join()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")

    save_reports(args.target, results)
    basic_vuln_check(results)

    print("\nScan Completed.")
