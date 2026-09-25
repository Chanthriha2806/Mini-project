from app import db
from app.models.setting import Setting

class SettingsController:
    """Controller to manage user configuration parameters such as thresholds and refresh rates."""

    @staticmethod
    def get_user_settings(user_id):
        """Fetches settings for a given user, seeding default values if not present."""
        settings = Setting.query.filter_by(user_id=user_id).first()
        if not settings:
            try:
                settings = Setting(
                    user_id=user_id,
                    cpu_threshold=90.0,
                    ram_threshold=90.0,
                    disk_threshold=95.0,
                    refresh_interval=5,
                    email_address=""
                )
                db.session.add(settings)
                db.session.commit()
            except Exception:
                db.session.rollback()
        return settings

    @staticmethod
    def update_user_settings(user, cpu_threshold, ram_threshold, disk_threshold, refresh_interval, email_address):
        """
        Validates preferences limits and commits updates to the database settings record.
        """
        # Validate constraints
        try:
            cpu = float(cpu_threshold)
            ram = float(ram_threshold)
            disk = float(disk_threshold)
            refresh = int(refresh_interval)
        except (ValueError, TypeError):
            return False, "Threshold values and refresh interval must be numerical."

        if not (10.0 <= cpu <= 100.0):
            return False, "CPU threshold must be between 10% and 100%."
        if not (10.0 <= ram <= 100.0):
            return False, "Memory (RAM) threshold must be between 10% and 100%."
        if not (10.0 <= disk <= 100.0):
            return False, "Disk space threshold must be between 10% and 100%."
        if not (2 <= refresh <= 300):
            return False, "Refresh interval must be between 2 and 300 seconds to ensure system stability."

        email_address = email_address.strip()
        if email_address and ("@" not in email_address or "." not in email_address):
            return False, "Please enter a valid email address configuration."

        try:
            settings = Setting.query.filter_by(user_id=user.id).first()
            if not settings:
                settings = Setting(user_id=user.id)
                db.session.add(settings)

            settings.cpu_threshold = cpu
            settings.ram_threshold = ram
            settings.disk_threshold = disk
            settings.refresh_interval = refresh
            settings.email_address = email_address if email_address else None

            db.session.commit()
            return True, "Monitoring configurations successfully updated."
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to commit settings: {str(e)}"

    @staticmethod
    def send_test_email(user, email_address):
        """Dispatches a test alert email to verify SMTP configuration and recipient setup."""
        email_address = (email_address or '').strip()
        if not email_address:
            settings = Setting.query.filter_by(user_id=user.id).first()
            if settings and settings.email_address:
                email_address = settings.email_address
            else:
                email_address = user.email

        if not email_address or "@" not in email_address:
            return False, "Please configure a valid recipient email address first."

        from app.utilities.mail_helper import MailHelper
        success = MailHelper.send_alert_email("TEST ALARM", 95.5, 90.0, target_email=email_address)
        if success:
            return True, f"Test alert email successfully dispatched to {email_address}!"
        else:
            return False, "Failed to dispatch test alert email. Please check SMTP settings."

