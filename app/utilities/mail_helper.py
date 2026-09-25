import logging
from flask import current_app
from flask_mail import Message
from app import mail

class MailHelper:
    """Helper service to format and transmit email alerts regarding resource usage threshold breaches."""

    @staticmethod
    def send_alert_email(metric_type, value, threshold, target_email=None):
        """Dispatches alert notifications via SMTP configuration when threshold is breached."""
        # Retrieve target configuration settings
        try:
            # Import settings inside method to prevent circular dependencies
            from app.models.setting import Setting
            
            # Use general settings target if available
            settings = Setting.query.order_by(Setting.id.asc()).first()
            recipient = target_email or (settings.email_address if settings and settings.email_address else current_app.config.get('MAIL_USERNAME'))

            
            if not recipient:
                logging.warning("No recipient email address configured. Skipping alert email dispatch.")
                return False

            subject = f"[CRITICAL BREACH] {metric_type} threshold exceeded!"
            body = (
                f"Dear Administrator,\n\n"
                f"This is an automated alert notification from your IT Infrastructure Monitoring Dashboard.\n\n"
                f"Metric: {metric_type}\n"
                f"Current Value: {value}%\n"
                f"Configured Threshold: {threshold}%\n"
                f"Timestamp: {current_app.config.get('CURRENT_TIME', 'Just now')}\n\n"
                f"Please login to your Monitoring Dashboard immediately to review recommending corrective actions.\n\n"
                f"Regards,\n"
                f"MonitorAI Engine"
            )

            # Check if SMTP details are configured
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                logging.info(f"[Mock Mail] Alert dispatched to {recipient}. SMTP details not set. Details: {metric_type}={value}%")
                return True

            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body
            )
            mail.send(msg)
            logging.info(f"Alert email successfully dispatched to {recipient} regarding {metric_type} breach.")
            return True

        except Exception as e:
            logging.error(f"Failed to dispatch alert notification email: {str(e)}")
            return False
