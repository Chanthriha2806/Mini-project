import os
import time
import socket
import platform
import psutil
from datetime import datetime

class SystemMonitor:
    """Utility service to extract system health diagnostics using psutil and platform APIs."""
    
    # Store previous counters to calculate network speeds dynamically without blocking
    _last_net_io = None
    _last_time = None

    @classmethod
    def get_network_speeds(cls):
        """Calculates current network upload and download speed in KB/s since the last invocation."""
        now = time.time()
        try:
            net_io = psutil.net_io_counters()
        except Exception:
            return 0.0, 0.0

        if cls._last_net_io is None or cls._last_time is None:
            cls._last_net_io = net_io
            cls._last_time = now
            return 0.0, 0.0

        elapsed = now - cls._last_time
        if elapsed <= 0:
            elapsed = 0.1

        bytes_sent = net_io.bytes_sent - cls._last_net_io.bytes_sent
        bytes_recv = net_io.bytes_recv - cls._last_net_io.bytes_recv

        # Speed in KB/s
        upload_speed = max(0.0, (bytes_sent / elapsed) / 1024.0)
        download_speed = max(0.0, (bytes_recv / elapsed) / 1024.0)

        # Update cache
        cls._last_net_io = net_io
        cls._last_time = now

        return upload_speed, download_speed

    @staticmethod
    def get_local_ip():
        """Gets local active IP address by connecting socket to public network (no data transfer)."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.2)
        try:
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    @staticmethod
    def get_mac_address(ip):
        """Gets the MAC address corresponding to the active interface IP."""
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                has_ip = False
                mac = None
                for addr in addrs:
                    if addr.family == socket.AF_INET and addr.address == ip:
                        has_ip = True
                    if addr.family == psutil.AF_LINK or (hasattr(psutil, 'AF_PACKET') and addr.family == psutil.AF_PACKET):
                        mac = addr.address
                if has_ip and mac:
                    return mac
            
            # Fallback: Find first valid MAC Address
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == psutil.AF_LINK or (hasattr(psutil, 'AF_PACKET') and addr.family == psutil.AF_PACKET):
                        return addr.address
        except Exception:
            pass
        return "00:00:00:00:00:00"

    @classmethod
    def get_system_metrics(cls):
        """Assembles all system diagnostics for CPU, Memory, Disk, Network, and Uptime."""
        # 1. CPU metrics
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count(logical=True)
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_frequency = cpu_freq.current if cpu_freq else 0.0
        except Exception:
            cpu_frequency = 0.0

        # 2. Memory metrics
        mem = psutil.virtual_memory()
        total_ram = mem.total / (1024**3)      # GB
        used_ram = mem.used / (1024**3)        # GB
        available_ram = mem.available / (1024**3) # GB
        ram_percent = mem.percent

        # 3. Disk metrics
        try:
            disk = psutil.disk_usage('/')
            total_disk = disk.total / (1024**3)  # GB
            used_disk = disk.used / (1024**3)    # GB
            free_disk = disk.free / (1024**3)    # GB
            disk_percent = disk.percent
        except Exception:
            total_disk, used_disk, free_disk, disk_percent = 0.0, 0.0, 0.0, 0.0

        # 4. Network speeds & info
        upload_speed, download_speed = cls.get_network_speeds()
        ip_addr = cls.get_local_ip()
        mac_addr = cls.get_mac_address(ip_addr)

        # 5. OS & Boot time details
        try:
            boot_time_timestamp = psutil.boot_time()
            boot_time_str = datetime.fromtimestamp(boot_time_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            uptime = max(0.0, time.time() - boot_time_timestamp)
        except Exception:
            boot_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            uptime = 0.0

        # Uptime formatting: Days, Hours, Minutes
        days = int(uptime // 86400)
        hours = int((uptime % 86400) // 3600)
        minutes = int((uptime % 3600) // 60)
        uptime_str = f"{days}d {hours}h {minutes}m"

        # 6. Active stats counts
        try:
            users_count = len(psutil.users())
        except Exception:
            users_count = 1

        try:
            processes_count = len(psutil.pids())
        except Exception:
            processes_count = 10

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
                'download_speed': round(download_speed, 2),
                'ip': ip_addr,
                'mac': mac_addr
            },
            'system': {
                'os': f"{platform.system()} {platform.release()}",
                'processor': platform.processor() or "Unknown",
                'hostname': socket.gethostname(),
                'boot_time': boot_time_str,
                'uptime_str': uptime_str,
                'uptime_seconds': uptime
            },
            'active_counts': {
                'users': users_count,
                'processes': processes_count
            }
        }

    @staticmethod
    def get_processes():
        """Fetches top 10 CPU/Memory consuming processes currently running."""
        if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
            return [
                {'pid': 1, 'name': 'systemd', 'username': 'root', 'cpu_percent': 0.8, 'memory_percent': 1.2},
                {'pid': 12, 'name': 'python3', 'username': 'vercel', 'cpu_percent': 1.5, 'memory_percent': 2.4},
                {'pid': 45, 'name': 'node', 'username': 'vercel', 'cpu_percent': 0.5, 'memory_percent': 3.1}
            ]
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info or {}
                    if not info.get('username'):
                        info['username'] = 'SYSTEM'
                    info['memory_percent'] = round(info.get('memory_percent') or 0.0, 2)
                    info['cpu_percent'] = round(info.get('cpu_percent') or 0.0, 2)
                    processes.append(info)
                except Exception:
                    continue
        except Exception:
            return []

        sorted_procs = sorted(processes, key=lambda x: x.get('cpu_percent', 0.0) or 0.0, reverse=True)
        return sorted_procs[:10]

