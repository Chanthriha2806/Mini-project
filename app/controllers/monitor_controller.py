import socket
import platform
try:
    import psutil
except ImportError:
    psutil = None
from app.utilities.system_monitor import SystemMonitor

class MonitorController:
    """Controller to query deep, structural system specs and details for the Monitoring module."""

    @staticmethod
    def get_detailed_system_specs():
        """Aggregates low-level diagnostic parameters for hardware, partitions, and network cards."""
        # 1. CPU properties
        try:
            cpu_stats = psutil.cpu_stats()
            ctx_switches = cpu_stats.ctx_switches
            interrupts = cpu_stats.interrupts
        except Exception:
            ctx_switches, interrupts = 0, 0

        cpu_physical_cores = psutil.cpu_count(logical=False) or 1
        cpu_logical_cores = psutil.cpu_count(logical=True) or 1

        # 2. Swap Memory properties
        try:
            swap = psutil.swap_memory()
            swap_total = swap.total / (1024**3)
            swap_used = swap.used / (1024**3)
            swap_free = swap.free / (1024**3)
            swap_percent = swap.percent
        except Exception:
            swap_total, swap_used, swap_free, swap_percent = 0.0, 0.0, 0.0, 0.0

        # 3. Virtual Memory (active/inactive) if supported
        mem = psutil.virtual_memory()
        active_mem = getattr(mem, 'active', 0) / (1024**3)
        inactive_mem = getattr(mem, 'inactive', 0) / (1024**3)

        # 4. Mounted disk partitions
        partitions = []
        try:
            for part in psutil.disk_partitions(all=False):
                # Filter out raw devices without mountpoints or locked mount points (like empty optical drives on Windows)
                if not part.mountpoint:
                    continue
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    partitions.append({
                        'device': part.device,
                        'mountpoint': part.mountpoint,
                        'fstype': part.fstype,
                        'opts': part.opts,
                        'total': round(usage.total / (1024**3), 2),
                        'used': round(usage.used / (1024**3), 2),
                        'free': round(usage.free / (1024**3), 2),
                        'percent': usage.percent
                    })
                except (PermissionError, FileNotFoundError):
                    # Windows floppy or locked recovery partitions can throw errors
                    continue
        except Exception:
            pass

        # 5. Network Interfaces Details
        interfaces = []
        try:
            net_addrs = psutil.net_if_addrs()
            net_stats = psutil.net_if_stats()
            
            for iface_name, addrs in net_addrs.items():
                stats = net_stats.get(iface_name)
                is_up = stats.isup if stats else False
                speed = stats.speed if stats else 0 # Mbps
                mtu = stats.mtu if stats else 1500

                ipv4 = None
                ipv6 = None
                mac = None

                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        ipv4 = addr.address
                    elif addr.family == socket.AF_INET6:
                        ipv6 = addr.address
                    elif addr.family == psutil.AF_LINK or (hasattr(psutil, 'AF_PACKET') and addr.family == psutil.AF_PACKET):
                        mac = addr.address

                # Only include interfaces that have a MAC address or IP to clean up results
                if ipv4 or mac:
                    interfaces.append({
                        'name': iface_name,
                        'is_up': is_up,
                        'speed': speed,
                        'mtu': mtu,
                        'ipv4': ipv4 or "N/A",
                        'ipv6': ipv6 or "N/A",
                        'mac': mac or "N/A"
                    })
        except Exception:
            pass

        # Get base telemetry parameters
        base_metrics = SystemMonitor.get_system_metrics()
        top_processes = SystemMonitor.get_processes()

        return {
            'cpu': {
                'usage': base_metrics['cpu']['usage'],
                'cores_physical': cpu_physical_cores,
                'cores_logical': cpu_logical_cores,
                'frequency': base_metrics['cpu']['frequency'],
                'ctx_switches': f"{ctx_switches:,}",
                'interrupts': f"{interrupts:,}"
            },
            'memory': {
                'total': base_metrics['memory']['total'],
                'used': base_metrics['memory']['used'],
                'available': base_metrics['memory']['available'],
                'percent': base_metrics['memory']['percent'],
                'swap_total': round(swap_total, 2),
                'swap_used': round(swap_used, 2),
                'swap_free': round(swap_free, 2),
                'swap_percent': swap_percent,
                'active': round(active_mem, 2),
                'inactive': round(inactive_mem, 2)
            },
            'partitions': partitions,
            'interfaces': interfaces,
            'system': {
                'os': base_metrics['system']['os'],
                'processor': base_metrics['system']['processor'],
                'hostname': base_metrics['system']['hostname'],
                'boot_time': base_metrics['system']['boot_time'],
                'uptime_str': base_metrics['system']['uptime_str'],
                'python_version': platform.python_version(),
                'machine': platform.machine()
            },
            'processes': top_processes
        }
