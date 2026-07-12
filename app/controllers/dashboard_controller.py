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
            settings = Setting.query.filter_by(user_id=user.id).first()
            cpu_thresh = settings.cpu_threshold if settings else 90.0
            ram_thresh = settings.ram_threshold if settings else 90.0
            disk_thresh = settings.disk_threshold if settings else 95.0

            cpu_val = metrics['cpu']['usage']
            ram_val = metrics['memory']['percent']
            disk_val = metrics['disk']['percent']

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

