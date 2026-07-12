from app import db
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

        return {
            'settings': settings,
            'active_alerts': active_alerts,
            'recent_alerts': recent_alerts
        }

    @classmethod
    def get_api_metrics(cls, user):
        """
        Retrieves real-time system metrics, audits them against configured settings,
        generates/resolves db alerts, logs metrics in history, and returns JSON statistics.
        """
        metrics = SystemMonitor.get_system_metrics()
        settings = Setting.query.filter_by(user_id=user.id).first()
        
        # Load thresholds (fallback to defaults if settings row is somehow missing)
        cpu_thresh = settings.cpu_threshold if settings else 90.0
        ram_thresh = settings.ram_threshold if settings else 90.0
        disk_thresh = settings.disk_threshold if settings else 95.0

        # Perform resource threshold auditing
        cpu_val = metrics['cpu']['usage']
        ram_val = metrics['memory']['percent']
        disk_val = metrics['disk']['percent']

        # Determine overall server status badge
        # Rule: Any critical breach sets Status to Critical. Else warning if close, else Healthy.
        status = "HEALTHY"
        reasons = []

        if cpu_val > cpu_thresh:
            status = "CRITICAL"
            reasons.append(f"CPU usage ({cpu_val}%) exceeds threshold of {cpu_thresh}%")
            cls._create_or_retain_alert('CPU', f"High CPU utilization detected: {cpu_val}%", cpu_val, cpu_thresh)
        else:
            cls._resolve_alert('CPU', f"CPU utilization returned to normal: {cpu_val}%")

        if ram_val > ram_thresh:
            status = "CRITICAL"
            reasons.append(f"RAM usage ({ram_val}%) exceeds threshold of {ram_thresh}%")
            cls._create_or_retain_alert('RAM', f"High Memory usage detected: {ram_val}%", ram_val, ram_thresh)
        else:
            cls._resolve_alert('RAM', f"Memory usage returned to normal: {ram_val}%")

        if disk_val > disk_thresh:
            status = "CRITICAL"
            reasons.append(f"Disk space usage ({disk_val}%) exceeds threshold of {disk_thresh}%")
            cls._create_or_retain_alert('DISK', f"Disk space usage critical: {disk_val}%", disk_val, disk_thresh)
        else:
            cls._resolve_alert('DISK', f"Disk space usage returned to normal: {disk_val}%")

        # Set Status to Warning if any of them are within 10% of their threshold
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

        # Log current metrics in MonitoringHistory for Chart.js rendering
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

            # Clean up old records (limit history to last 200 entries to prevent DB bloating)
            # Find the ID of the 200th record back
            records_count = MonitoringHistory.query.count()
            if records_count > 200:
                oldest_to_keep = MonitoringHistory.query.order_by(MonitoringHistory.created_at.desc()).offset(200).first()
                if oldest_to_keep:
                    MonitoringHistory.query.filter(MonitoringHistory.created_at <= oldest_to_keep.created_at).delete()
                    db.session.commit()
        except Exception:
            db.session.rollback()

        return metrics

    @staticmethod
    def get_api_historical_metrics():
        """Fetches the last 20 logged historical data coordinates for the line charts."""
        # Grab last 20 items ordered by ID ascending (chronological order)
        subquery = MonitoringHistory.query.order_by(MonitoringHistory.created_at.desc()).limit(20).all()
        # Reverse to chronologically ascending for Chart.js logic
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

