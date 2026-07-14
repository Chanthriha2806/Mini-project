from app import db
from app.models.user import User
from app.models.setting import Setting
from app.models.alert import Alert
from app.models.monitoring import MonitoringHistory
from app.utilities.system_monitor import SystemMonitor
from datetime import datetime, timedelta

class DashboardController:
    """Controller to manage dashboard analytics, historical logging, and health threshold checks."""

    @staticmethod
    def get_dashboard_data(user):
        """Prepares initial data load for the dashboard templates."""
        # Retrieve user settings
        settings = Setting.query.filter_by(user_id=user.id).first()
        if not settings:
            # Fallback (though registered users should always have settings seeded)
            settings = Setting(
                user_id=user.id,
                cpu_threshold=90.0,
                ram_threshold=90.0,
                disk_threshold=95.0,
                refresh_interval=5,
                email_address=user.email
            )
            db.session.add(settings)
            db.session.commit()

        # Retrieve active alerts
        active_alerts = Alert.query.filter_by(status='ACTIVE').order_by(Alert.created_at.desc()).all()
        recent_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(10).all()

        # Retrieve registered client devices for admin dropdown
        devices = []
        if user.is_admin:
            unique_devices = db.session.query(
                MonitoringHistory.user_id, 
                MonitoringHistory.hostname
            ).filter(MonitoringHistory.user_id != None).distinct().all()
            
            for dev_user_id, dev_hostname in unique_devices:
                dev_user = User.query.get(dev_user_id)
                if dev_user:
                    devices.append({
                        'user_id': dev_user_id,
                        'username': dev_user.username,
                        'hostname': dev_hostname
                    })

        return {
            'settings': settings,
            'active_alerts': active_alerts,
            'recent_alerts': recent_alerts,
            'devices': devices
        }

    @classmethod
    def get_api_metrics(cls, user, user_id=None, hostname=None):
        """
        Retrieves real-time system metrics (either local or from remote client reports),
        audits them against thresholds, generates alerts, and returns telemetry dict.
        """
        # If user is admin and requested specific client, or if user is non-admin who has remote reports
        target_user_id = user_id if (user.is_admin and user_id) else (None if user.is_admin else user.id)
        target_hostname = hostname if (user.is_admin and hostname) else None
        
        latest = None
        if target_user_id or target_hostname:
            query = MonitoringHistory.query.filter(MonitoringHistory.user_id != None)
            if target_user_id:
                query = query.filter_by(user_id=target_user_id)
            if target_hostname:
                query = query.filter_by(hostname=target_hostname)
            latest = query.order_by(MonitoringHistory.created_at.desc()).first()

        if latest:
            # Reconstruct metrics payload from the latest database entry
            metrics = {
                'cpu': {
                    'usage': latest.cpu_usage,
                    'cores': 'N/A',
                    'frequency': 0.0
                },
                'memory': {
                    'total': 0.0,
                    'used': 0.0,
                    'available': 0.0,
                    'percent': latest.ram_usage
                },
                'disk': {
                    'total': 0.0,
                    'used': 0.0,
                    'free': 0.0,
                    'percent': latest.disk_usage
                },
                'network': {
                    'upload_speed': latest.upload_speed,
                    'download_speed': latest.download_speed
                },
                'system': {
                    'os': 'Client OS',
                    'processor': 'Remote Agent',
                    'hostname': latest.hostname,
                    'boot_time': 'N/A',
                    'uptime_str': 'Active'
                }
            }
            metrics['is_remote'] = True
            
            # Load thresholds for auditing
            settings = Setting.query.filter_by(user_id=latest.user_id).first()
            cpu_thresh = settings.cpu_threshold if settings else 90.0
            ram_thresh = settings.ram_threshold if settings else 90.0
            disk_thresh = settings.disk_threshold if settings else 95.0

            cpu_val = latest.cpu_usage
            ram_val = latest.ram_usage
            disk_val = latest.disk_usage
        else:
            # Fallback to local machine metrics
            metrics = SystemMonitor.get_system_metrics()
            metrics['is_remote'] = False
            settings = Setting.query.filter_by(user_id=user.id).first()
            cpu_thresh = settings.cpu_threshold if settings else 90.0
            ram_thresh = settings.ram_threshold if settings else 90.0
            disk_thresh = settings.disk_threshold if settings else 95.0

            cpu_val = metrics['cpu']['usage']
            ram_val = metrics['memory']['percent']
            disk_val = metrics['disk']['percent']

        # Get history records for regression
        history_query = MonitoringHistory.query
        if target_user_id or target_hostname:
            history_query = history_query.filter(MonitoringHistory.user_id != None)
            if target_user_id:
                history_query = history_query.filter_by(user_id=target_user_id)
            if target_hostname:
                history_query = history_query.filter_by(hostname=target_hostname)
        else:
            history_query = history_query.filter(MonitoringHistory.user_id == None)
        
        history_records = history_query.order_by(MonitoringHistory.created_at.desc()).limit(20).all()
        history_records = list(reversed(history_records))
        
        disk_pred_msg, disk_pred_level = cls._predict_disk_exhaustion(history_records)
        metrics['disk']['prediction'] = disk_pred_msg
        metrics['disk']['prediction_level'] = disk_pred_level

        # Determine overall server status badge
        status = "HEALTHY"
        reasons = []

        if cpu_val > cpu_thresh:
            status = "CRITICAL"
            reasons.append(f"CPU usage ({cpu_val}%) exceeds threshold of {cpu_thresh}%")
            if not latest: # Only generate server alerts for local machine metrics
                cls._create_or_retain_alert('CPU', f"High CPU utilization detected: {cpu_val}%", cpu_val, cpu_thresh)
        else:
            if not latest:
                cls._resolve_alert('CPU', f"CPU utilization returned to normal: {cpu_val}%")

        if ram_val > ram_thresh:
            status = "CRITICAL"
            reasons.append(f"RAM usage ({ram_val}%) exceeds threshold of {ram_thresh}%")
            if not latest:
                cls._create_or_retain_alert('RAM', f"High Memory usage detected: {ram_val}%", ram_val, ram_thresh)
        else:
            if not latest:
                cls._resolve_alert('RAM', f"Memory usage returned to normal: {ram_val}%")

        if disk_val > disk_thresh:
            status = "CRITICAL"
            reasons.append(f"Disk space usage ({disk_val}%) exceeds threshold of {disk_thresh}%")
            if not latest:
                cls._create_or_retain_alert('DISK', f"Disk space usage critical: {disk_val}%", disk_val, disk_thresh)
        else:
            if not latest:
                cls._resolve_alert('DISK', f"Disk space usage returned to normal: {disk_val}%")

        if status != "CRITICAL":
            if (cpu_val > cpu_thresh - 10.0) or (ram_val > ram_thresh - 10.0) or (disk_val > disk_thresh - 10.0):
                status = "WARNING"

        metrics['health_status'] = status
        metrics['health_reasons'] = reasons

        # Generate AI diagnostics recommendations
        from app.utilities.ai_engine import RecommendationEngine
        metrics['recommendations'] = RecommendationEngine.generate_recommendations(
            cpu_val,
            ram_val,
            disk_val,
            metrics['network']['upload_speed'],
            metrics['network']['download_speed'],
            status
        )

        # Log current local metrics (if it's not a remote client query)
        if not latest:
            try:
                history_record = MonitoringHistory(
                    cpu_usage=cpu_val,
                    ram_usage=ram_val,
                    disk_usage=disk_val,
                    upload_speed=metrics['network']['upload_speed'],
                    download_speed=metrics['network']['download_speed']
                )
                db.session.add(history_record)
                db.session.commit()

                # Clean up old records
                records_count = MonitoringHistory.query.filter(MonitoringHistory.user_id == None).count()
                if records_count > 200:
                    oldest_to_keep = MonitoringHistory.query.filter(MonitoringHistory.user_id == None)\
                        .order_by(MonitoringHistory.created_at.desc()).offset(200).first()
                    if oldest_to_keep:
                        MonitoringHistory.query.filter(MonitoringHistory.user_id == None)\
                            .filter(MonitoringHistory.created_at <= oldest_to_keep.created_at).delete()
                        db.session.commit()
            except Exception:
                db.session.rollback()

        return metrics

    @staticmethod
    def get_api_historical_metrics(user, user_id=None, hostname=None):
        """Fetches the last 20 logged historical data coordinates for the line charts."""
        query = MonitoringHistory.query
        
        target_user_id = user_id if (user.is_admin and user_id) else (None if user.is_admin else user.id)
        target_hostname = hostname if (user.is_admin and hostname) else None

        if target_user_id or target_hostname:
            query = query.filter(MonitoringHistory.user_id != None)
            if target_user_id:
                query = query.filter_by(user_id=target_user_id)
            if target_hostname:
                query = query.filter_by(hostname=target_hostname)
        else:
            query = query.filter(MonitoringHistory.user_id == None)

        subquery = query.order_by(MonitoringHistory.created_at.desc()).limit(20).all()
        history = list(reversed(subquery))

        data = {
            'labels': [h.created_at.strftime('%H:%M:%S') for h in history],
            'cpu': [h.cpu_usage for h in history],
            'ram': [h.ram_usage for h in history],
            'disk': [h.disk_usage for h in history],
            'upload': [h.upload_speed for h in history],
            'download': [h.download_speed for h in history]
        }
        return data

    @staticmethod
    def save_client_metrics(user, data, remote_ip):
        """Saves telemetry payload sent from a remote client agent."""
        try:
            cpu_val = float(data.get('cpu', {}).get('usage', 0.0))
            ram_val = float(data.get('memory', {}).get('percent', 0.0))
            disk_val = float(data.get('disk', {}).get('percent', 0.0))
            upload_speed = float(data.get('network', {}).get('upload_speed', 0.0))
            download_speed = float(data.get('network', {}).get('download_speed', 0.0))
            hostname = data.get('system', {}).get('hostname', 'Unknown')

            # Create history record
            history_record = MonitoringHistory(
                cpu_usage=cpu_val,
                ram_usage=ram_val,
                disk_usage=disk_val,
                upload_speed=upload_speed,
                download_speed=download_speed,
                user_id=user.id,
                hostname=hostname,
                ip_address=remote_ip
            )
            db.session.add(history_record)
            db.session.commit()

            # Clean up history for this user & host to prevent DB bloating (max 200 logs)
            records_count = MonitoringHistory.query.filter_by(user_id=user.id, hostname=hostname).count()
            if records_count > 200:
                oldest_to_keep = MonitoringHistory.query.filter_by(user_id=user.id, hostname=hostname)\
                    .order_by(MonitoringHistory.created_at.desc()).offset(200).first()
                if oldest_to_keep:
                    MonitoringHistory.query.filter_by(user_id=user.id, hostname=hostname)\
                        .filter(MonitoringHistory.created_at <= oldest_to_keep.created_at).delete()
                    db.session.commit()

            # Also check thresholds for client to generate alerts if needed
            settings = Setting.query.filter_by(user_id=user.id).first()
            cpu_thresh = settings.cpu_threshold if settings else 90.0
            ram_thresh = settings.ram_threshold if settings else 90.0
            disk_thresh = settings.disk_threshold if settings else 95.0

            alert_prefix = f"[{hostname}] "
            if cpu_val > cpu_thresh:
                DashboardController._create_or_retain_alert(
                    f'CPU_{user.id}_{hostname}', 
                    f"{alert_prefix}High CPU utilization: {cpu_val}%", 
                    cpu_val, 
                    cpu_thresh
                )
            else:
                DashboardController._resolve_alert(f'CPU_{user.id}_{hostname}', f"CPU utilization normal on {hostname}")

            if ram_val > ram_thresh:
                DashboardController._create_or_retain_alert(
                    f'RAM_{user.id}_{hostname}', 
                    f"{alert_prefix}High RAM usage: {ram_val}%", 
                    ram_val, 
                    ram_thresh
                )
            else:
                DashboardController._resolve_alert(f'RAM_{user.id}_{hostname}', f"RAM utilization normal on {hostname}")

            if disk_val > disk_thresh:
                DashboardController._create_or_retain_alert(
                    f'DISK_{user.id}_{hostname}', 
                    f"{alert_prefix}High disk space usage: {disk_val}%", 
                    disk_val, 
                    disk_thresh
                )
            else:
                DashboardController._resolve_alert(f'DISK_{user.id}_{hostname}', f"Disk utilization normal on {hostname}")

            return True, "Metrics saved successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to save metrics: {str(e)}"

    @staticmethod
    def _create_or_retain_alert(metric_type, message, value, threshold):
        """Helper to create a new alarm record or keep an existing ACTIVE one."""
        try:
            active_alert = Alert.query.filter_by(metric_type=metric_type, status='ACTIVE').first()
            if not active_alert:
                new_alert = Alert(
                    metric_type=metric_type,
                    message=message,
                    value=value,
                    threshold=threshold,
                    status='ACTIVE'
                )
                db.session.add(new_alert)
                db.session.commit()
                
                # Proactively trigger an email alert when a new alert is generated
                from app.utilities.mail_helper import MailHelper
                MailHelper.send_alert_email(metric_type, value, threshold)
        except Exception:
            db.session.rollback()

    @staticmethod
    def _resolve_alert(metric_type, message):
        """Helper to set status of an ACTIVE alarm record to RESOLVED once metric recovers."""
        try:
            active_alert = Alert.query.filter_by(metric_type=metric_type, status='ACTIVE').first()
            if active_alert:
                active_alert.status = 'RESOLVED'
                db.session.commit()
        except Exception:
            db.session.rollback()

    @staticmethod
    def clear_resolved_alerts():
        """Deletes all RESOLVED alerts from the alerts table database to purge history logs."""
        try:
            Alert.query.filter_by(status='RESOLVED').delete()
            db.session.commit()
            return True, "Resolved alerts log history cleared successfully."
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to clear alerts log: {str(e)}"

    @staticmethod
    def _predict_disk_exhaustion(history_records):
        """Calculates estimated time until disk space is fully depleted (100% usage) using linear regression."""
        if len(history_records) < 5:
            return "Awaiting telemetry data...", "info"
        
        # Convert times to elapsed seconds and disk usage values
        t0 = history_records[0].created_at
        x = []
        y = []
        for r in history_records:
            x.append((r.created_at - t0).total_seconds())
            y.append(r.disk_usage)
            
        N = len(history_records)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        denom = (N * sum_x2) - (sum_x ** 2)
        if denom == 0:
            return "Disk usage stable", "success"
            
        slope = (N * sum_xy - sum_x * sum_y) / denom
        
        if slope <= 0:
            return "Disk usage stable", "success"
            
        last_y = y[-1]
        if last_y >= 100:
            return "Disk storage exhausted!", "danger"
            
        seconds_left = (100.0 - last_y) / slope
        
        if seconds_left < 60:
            return f"Est. exhaustion in {int(seconds_left)} seconds!", "danger"
        elif seconds_left < 3600:
            return f"Est. exhaustion in {int(seconds_left // 60)} minutes!", "danger"
        elif seconds_left < 86400:
            hours = round(seconds_left / 3600, 1)
            return f"Est. exhaustion in {hours} hours!", "warning"
        else:
            days = round(seconds_left / 86400, 1)
            level = "warning" if days < 7 else "success"
            return f"Est. exhaustion in {days} days", level

    @staticmethod
    def kill_process(user, pid):
        """Terminates a runaway system process by PID. Restricted to admin users."""
        if not user.is_admin:
            return False, "Access denied. Only administrators can terminate running processes."
        try:
            import psutil
            proc = psutil.Process(pid)
            proc_name = proc.name()
            # Prevent killing system critical processes to avoid server crashes
            critical_names = ['system', 'idle', 'registry', 'smss.exe', 'csrss.exe', 'wininit.exe', 'services.exe', 'lsass.exe']
            if proc_name.lower() in critical_names:
                return False, f"Termination of system critical process '{proc_name}' is blocked."
            
            proc.terminate()
            try:
                proc.wait(timeout=1.0)
            except psutil.TimeoutExpired:
                proc.kill()
            return True, f"Process {proc_name} (PID {pid}) was successfully terminated."
        except psutil.NoSuchProcess:
            return False, f"No active process found with PID {pid}."
        except psutil.AccessDenied:
            return False, f"OS Access Denied: Insufficient permissions to kill PID {pid}."
        except Exception as e:
            return False, f"Failed to terminate process: {str(e)}"

    @staticmethod
    def chat_with_ai(user, message, current_metrics):
        """
        Formulates a context-aware markdown diagnostics report based on system telemetry.
        """
        msg = message.lower()
        
        cpu_val = current_metrics.get('cpu', {}).get('usage', 0.0)
        ram_val = current_metrics.get('memory', {}).get('percent', 0.0)
        disk_val = current_metrics.get('disk', {}).get('percent', 0.0)
        
        up_speed = current_metrics.get('network', {}).get('upload_speed', 0.0)
        down_speed = current_metrics.get('network', {}).get('download_speed', 0.0)
        hostname = current_metrics.get('system', {}).get('hostname', 'Localhost')
        os_name = current_metrics.get('system', {}).get('os', 'Unknown')
        
        alerts_list = Alert.query.filter_by(status='ACTIVE').all()
        alerts_count = len(alerts_list)
        
        top_proc_str = "None"
        processes = current_metrics.get('processes', [])
        if not processes:
            from app.utilities.system_monitor import SystemMonitor
            processes = SystemMonitor.get_processes()
            
        if processes:
            top_proc = processes[0]
            top_proc_str = f"`{top_proc.get('name')}` (PID: {top_proc.get('pid')}, CPU: {top_proc.get('cpu_percent')}%, RAM: {top_proc.get('memory_percent')}%)"
        
        if any(w in msg for w in ['cpu', 'processor', 'load', 'utilization']):
            response = f"### 🖥️ CPU Diagnostics Report for **{hostname}**\n\n"
            response += f"* **Current Usage**: `{cpu_val}%`\n"
            response += f"* **CPU Core Blocks**: `{current_metrics.get('cpu', {}).get('cores', 'N/A')}` logical processors\n"
            response += f"* **Current Frequency**: `{current_metrics.get('cpu', {}).get('frequency', 'N/A')} GHz`\n"
            response += f"* **Primary Resource Consumer**: {top_proc_str}\n\n"
            response += "#### 🔍 Analysis & Recommendations:\n"
            if cpu_val > 90:
                response += f"1. 🚨 **Critical Core Saturation detected!** The CPU is operating above the safe threshold.\n"
                response += f"2. The runaway process **{top_proc_str}** is taking up significant cycles.\n"
                response += f"3. **Action Item**: Go to the **Processes** section on the dashboard and click **Kill** on the runaway task.\n"
                response += f"4. If this is a recurring load, consider scaling the hardware or scheduling non-critical background updates to off-peak periods."
            elif cpu_val > 70:
                response += f"1. ⚠️ **Moderate-to-high workload.** CPU usage is slightly elevated.\n"
                response += f"2. The primary loader is **{top_proc_str}**.\n"
                response += f"3. **Action Item**: Check for unnecessary background applications, browser threads, or dev compilation pipelines that can be closed."
            else:
                response += f"1. ✅ **All clear.** CPU utilization is optimal and within standard tolerances. No troubleshooting actions are needed."
                
        elif any(w in msg for w in ['ram', 'memory', 'physical memory']):
            used_mem = current_metrics.get('memory', {}).get('used', 0.0)
            total_mem = current_metrics.get('memory', {}).get('total', 0.0)
            response = f"### 💾 Memory Diagnostics Report for **{hostname}**\n\n"
            response += f"* **RAM Allocation**: `{ram_val}%`\n"
            response += f"* **Usage Footprint**: `{used_mem} GB` used of `{total_mem} GB` total\n"
            response += f"* **Primary Resource Consumer**: {top_proc_str}\n\n"
            response += "#### 🔍 Analysis & Recommendations:\n"
            if ram_val > 90:
                response += f"1. 🚨 **RAM Depletion Warning!** Physical memory is almost fully exhausted.\n"
                response += f"2. Highly active processes like **{top_proc_str}** are consuming a lot of heap space.\n"
                response += f"3. **Action Item**: Terminate leaking daemons or stop heavy active virtual machines/docker stacks.\n"
                response += f"4. Consider scaling physical RAM modules on this node to sustain this load."
            elif ram_val > 75:
                response += f"1. ⚠️ **Elevated memory occupancy.**\n"
                response += f"2. **Action Item**: Check if there are dangling browser or service instances that can be restarted to free up buffers and memory caching pools."
            else:
                response += f"1. ✅ **Memory status Healthy.** Current RAM utilization is stable. Buffer cache is working optimally."

        elif any(w in msg for w in ['disk', 'storage', 'partition', 'space']):
            pred_msg = current_metrics.get('disk', {}).get('prediction', 'No historical trend records found')
            used_disk = current_metrics.get('disk', {}).get('used', 0.0)
            total_disk = current_metrics.get('disk', {}).get('total', 0.0)
            response = f"### 💽 Disk Storage Diagnostics Report for **{hostname}**\n\n"
            response += f"* **Storage Occupancy**: `{disk_val}%` (`{used_disk} GB` used / `{total_disk} GB` total)\n"
            response += f"* **Predictive Runout Estimate**: **{pred_msg}**\n\n"
            response += "#### 🔍 Analysis & Recommendations:\n"
            if disk_val > 95:
                response += f"1. 🚨 **Critical Storage Exhaustion!** The root partition is nearly full.\n"
                response += f"2. **Action Item**: Trigger a disk cleanup utility on node **{hostname}** to empty the system trash and temp directories.\n"
                response += f"3. Clean out orphaned docker images/volumes: `docker system prune -a`\n"
                response += f"4. Transfer archived logs or diagnostic core dumps to a secondary storage device or cloud bucket."
            elif disk_val > 80:
                response += f"1. ⚠️ **Low disk space warning.**\n"
                response += f"2. **Action Item**: Audit folder tree structures to identify large files. Clean up local package directories (e.g. `.npm`, `.pip` caches)."
            else:
                response += f"1. ✅ **Storage space is adequate.** The filesystem has sufficient free blocks to perform standard file read/write operations."

        elif any(w in msg for w in ['network', 'speed', 'bandwidth', 'upload', 'download', 'ip']):
            response = f"### 🌐 Network Interface Diagnostics for **{hostname}**\n\n"
            response += f"* **Active IP Address**: `{current_metrics.get('network', {}).get('ip', 'N/A')}`\n"
            response += f"* **Active MAC Address**: `{current_metrics.get('network', {}).get('mac', 'N/A')}`\n"
            response += f"* **Current Speeds**: Upload: `{up_speed} KB/s` | Download: `{down_speed} KB/s`\n\n"
            response += "#### 🔍 Analysis & Recommendations:\n"
            if up_speed > 10240 or down_speed > 20480:
                response += f"1. ⚠️ **High throughput activity detected.**\n"
                response += f"2. Active uploads (`{round(up_speed/1024, 1)} MB/s`) or downloads (`{round(down_speed/1024, 1)} MB/s`) are consuming a portion of your local gateway capacity.\n"
                response += f"3. Check for background synchronizations (Google Drive, OneDrive) or file-sharing protocols."
            else:
                response += f"1. ✅ **Network traffic is normal.** Interface throughput is stable and socket connections are reacting without latency bottlenecks."

        elif any(w in msg for w in ['alert', 'warning', 'error', 'breach', 'critical']):
            response = f"### 🔔 Alerts & Alarms Status Report\n\n"
            response += f"* **Active Alert Counts**: `{alerts_count} Active Alerts`\n\n"
            response += "#### 🔍 Active Alert List:\n"
            if alerts_list:
                for idx, alert in enumerate(alerts_list, 1):
                    response += f"\n{idx}. 🚨 **{alert.metric_type} Breach**: {alert.message} (Limit: `{alert.threshold}%` | Value: `{alert.value}%`)\n"
                response += "\n**Action Recommendation**: Investigate the corresponding metric card above or click **Clear Logs** on the Feed Panel to flush resolved alarm metrics."
            else:
                response += f"\n✅ **Zero breaches registered.** All telemetry parameters are executing within safe parameters."

        elif any(w in msg for w in ['process', 'kill', 'terminate', 'runaway', 'pid']):
            response = f"### ⚙️ Process Management Diagnostics\n\n"
            response += f"Here are the top resource-consuming tasks executing on **{hostname}**:\n\n"
            response += "| PID | Process Name | User | CPU % | Memory % |\n"
            response += "|---|---|---|---|---|\n"
            for p in processes[:5]:
                response += f"| `{p.get('pid')}` | **{p.get('name')}** | {p.get('username')} | `{p.get('cpu_percent')}%` | `{p.get('memory_percent')}%` |\n"
                
            response += f"\n#### 🔍 Troubleshooting Runaway Processes:\n"
            response += f"1. Identify the task with the highest CPU/Memory footprint. In this case, **{top_proc_str}** is primary.\n"
            response += f"2. If you are logged in as an Administrator, you can terminate it directly by clicking the **\"Kill\"** button in the **Top Running Processes** dashboard panel.\n"
            response += f"3. Terminal fallback command:\n"
            response += f"   * **Windows (PowerShell)**: `Stop-Process -Id <PID> -Force`\n"
            response += f"   * **Linux/macOS**: `kill -9 <PID>`\n"
        else:
            response = f"### 🤖 MonitorAI Diagnostics Assistant\n\n"
            response += f"Hello! I am your real-time IT Infrastructure Diagnostics assistant. I analyze the performance metrics of the **{hostname}** server node running **{os_name}**.\n\n"
            response += f"Here is a quick snapshot of the system health:\n"
            response += f"* **Overall Status**: `{current_metrics.get('health_status', 'UNKNOWN')}`\n"
            response += f"* **CPU Usage**: `{cpu_val}%` | **Memory**: `{ram_val}%` | **Disk**: `{disk_val}%`\n"
            response += f"* **Active Alerts**: `{alerts_count}` triggers active\n\n"
            response += f"#### 💡 Suggested Diagnostics Queries:\n"
            response += f"* 🖥️ *\"Tell me about the CPU load\"*\n"
            response += f"* 💾 *\"Is memory usage high?\"*\n"
            response += f"* 💽 *\"Check storage space limits\"*\n"
            response += f"* ⚙ *\"Show running processes\"*\n"
            response += f"* 🌐 *\"Check network speed status\"*\n"
        return response


