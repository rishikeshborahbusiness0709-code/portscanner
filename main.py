import socket
from datetime import datetime

# ===============================
# ASCII BANNER
# ===============================
def show_banner():
    print(r"""
   ____   ____  ____  _____ _____   _____ _____ _____ _   _ _____ _____ 
  |  _ \ / __ \|  _ \|  __ \_   _| |_   _|_   _/ ____| \ | |_   _/ ____|
  | |_) | |  | | |_) | |__) || |     | |   | || |    |  \| | | || |     
  |  _ <| |  | |  _ <|  ___/ | |     | |   | || |    | . ` | | || |     
  | |_) | |__| | |_) | |    _| |_   _| |_ _| || |____| |\  |_| || |____ 
  |____/ \____/|____/|_|   |_____| |_____|_____\_____|_| \_|_____\_____|

                PORT - SCANNER
                Created by whitedevil
    """)
    print("=" * 70)


# ===============================
# PORT SCAN FUNCTION
# ===============================
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False


# ===============================
# HTML REPORT GENERATION
# ===============================
def generate_report(ip, open_ports):
    with open("report.html", "w") as f:
        f.write("""
        <html>
        <head>
            <title>Port Scanner Report</title>
            <style>
                body { background-color:black; color:#00ff00; font-family:monospace; }
                h1 { color:#00ff00; }
            </style>
        </head>
        <body>
        """)
        f.write("<h1>PORT SCANNER REPORT</h1>")
        f.write(f"<p><strong>Target:</strong> {ip}</p>")
        f.write("<ul>")
        for port in open_ports:
            f.write(f"<li>Port {port} is OPEN</li>")
        f.write("</ul>")
        f.write("</body></html>")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    show_banner()

    target = input("Enter target IP (example 127.0.0.1): ")

    print(f"\nScanning {target}...")
    start_time = datetime.now()

    open_ports = []

    for port in range(20, 1025):
        if scan_port(target, port):
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)

    generate_report(target, open_ports)

    end_time = datetime.now()

    print("\nScan completed.")
    print("Time taken:", end_time - start_time)
    print("Report saved as report.html")
