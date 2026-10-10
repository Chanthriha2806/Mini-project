import time
import socket
import getpass
import sys

try:
    import psutil
except ImportError:
    print("[!] Error: 'psutil' is not installed. Please run 'pip install psutil' first.")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("[!] Error: 'requests' is not installed. Please run 'pip install requests' first.")
    sys.exit(1)

# Cache variables to calculate network speeds dynamically
_last_net_io = None
_last_time = None

def get_network_speeds():
    """Calculates upload and download speeds in KB/s."""
    global _last_net_io, _last_time
    now = time.time()
    try:
        net_io = psutil.net_io_counters()
    except Exception:
        return 0.0, 0.0

    if _last_net_io is None or _last_time is None:
        _last_net_io = net_io
        _last_time = now
        return 0.0, 0.0

    elapsed = now - _last_time
    if elapsed <= 0:
        elapsed = 0.1

    bytes_sent = net_io.bytes_sent - _last_net_io.bytes_sent
    bytes_recv = net_io.bytes_recv - _last_net_io.bytes_recv

    # Speed in KB/s
    upload_speed = max(0.0, (bytes_sent / elapsed) / 1024.0)
    download_speed = max(0.0, (bytes_recv / elapsed) / 1024.0)

    _last_net_io = net_io
    _last_time = now

    return upload_speed, download_speed

def get_system_metrics():
    """Gathers system metrics of the client machine using psutil."""
    # 1. CPU metrics
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_count = psutil.cpu_count(logical=True)
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_frequency = cpu_freq.current if cpu_freq else 0.0
    except Exception:
        cpu_frequency = 0.0

    # 2. RAM metrics
    mem = psutil.virtual_memory()
    total_ram = mem.total / (1024**3)
    used_ram = mem.used / (1024**3)
    available_ram = mem.available / (1024**3)
    ram_percent = mem.percent

    # 3. Disk metrics
    try:
        disk = psutil.disk_usage('/')
        total_disk = disk.total / (1024**3)
        used_disk = disk.used / (1024**3)
        free_disk = disk.free / (1024**3)
        disk_percent = disk.percent
    except Exception:
        total_disk, used_disk, free_disk, disk_percent = 0.0, 0.0, 0.0, 0.0

    # 4. Network metrics
    upload_speed, download_speed = get_network_speeds()

    return {
        'cpu': {
            'usage': cpu_usage,
            'cores': cpu_count,
            'frequency': round(cpu_frequency, 2)
        },
        'memory': {
            'total': round(total_ram, 2),
            'used': round(used_ram, 2),
            'available': round(available_ram, 2),
            'percent': ram_percent
        },
        'disk': {
            'total': round(total_disk, 2),
            'used': round(used_disk, 2),
            'free': round(free_disk, 2),
            'percent': disk_percent
        },
        'network': {
            'upload_speed': round(upload_speed, 2),
            'download_speed': round(download_speed, 2)
        },
        'system': {
            'hostname': socket.gethostname()
        }
    }

def main():
    print("====================================================")
    print("           MonitorAI Remote Client Agent            ")
    print("====================================================")

    # Default parameters
    server_url = "http://localhost:5000"
    username_email = "client"
    password = "client123"

    # Allow CLI overrides: client_agent.py [url] [username] [password]
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    if len(sys.argv) > 2:
        username_email = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]

    # Explicit interactive option
    if '--interactive' in sys.argv:
        server_url_input = input("Enter Server URL (default: http://localhost:5000): ").strip()
        if server_url_input:
            server_url = server_url_input
        username_email = input("Username or Email: ").strip()
        password = getpass.getpass("Password: ")

    if server_url.endswith("/"):
        server_url = server_url[:-1]

    session = requests.Session()
    session.headers.update({
        'Bypass-Tunnel-Reminder': 'true',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    login_url = f"{server_url}/auth/login"

    print("\n[*] Authenticating with server...")
    try:
        payload = {
            'username_email': username_email,
            'password': password
        }
        # Attempt to sign in
        response = session.post(login_url, data=payload, allow_redirects=False)

        # Flask-Login redirects with 302 on successful login
        if response.status_code == 302:
            print("[+] Login Successful!")
        elif response.status_code == 200 and "Invalid" not in response.text:
            print("[+] Login Successful!")
        else:
            print("[-] Login Failed: Invalid username or password.")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to connect to server: {e}")
        sys.exit(1)

        # Handle direct CLI ticket submission option
        if '--ticket' in sys.argv:
            ticket_idx = sys.argv.index('--ticket')
            sub = sys.argv[ticket_idx + 1] if len(sys.argv) > ticket_idx + 1 else f"Hardware issue from {socket.gethostname()}"
            desc = sys.argv[ticket_idx + 2] if len(sys.argv) > ticket_idx + 2 else "Laptop resource issue reported from remote client agent terminal."
            
            ticket_url = f"{server_url}/api/tickets/create"
            t_res = session.post(ticket_url, json={'subject': sub, 'description': desc})
            if t_res.status_code == 200:
                print(f"[+] Support Ticket Created Successfully! ({t_res.json().get('message')})")
            else:
                print(f"[-] Failed to submit support ticket: {t_res.text}")
            sys.exit(0)

    report_url = f"{server_url}/api/metrics/report"
    print(f"\n[*] Telemetry reporting started (Interval: 5s)...")
    print("[*] Press Ctrl+C to terminate the client agent.\n")

    # Initial dummy run to compute initial network speed delta
    get_network_speeds()
    time.sleep(1)

    while True:
        try:
            metrics = get_system_metrics()
            res = session.post(report_url, json=metrics)
            if res.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] Metrics reported successfully. (CPU: {metrics['cpu']['usage']}%, RAM: {metrics['memory']['percent']}%)")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Server returned status {res.status_code}: {res.text}")
            
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[+] Gracefully exiting agent. Goodbye!")
            break
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Network error: {e}")
            time.sleep(10)

if __name__ == '__main__':
    main()
