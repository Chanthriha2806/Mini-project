import logging
from flask import current_app
from flask_mail import Message
from app import mail

class MailHelper:
    """Helper service to format and transmit email alerts regarding resource usage threshold breaches."""

    @staticmethod
    def send_performance_alert(target_email, metric_type=None, value=None, threshold=None):
        """
        Dispatches automated performance alert to client when CPU or RAM utilization exceeds threshold.
        Subject: Laptop Performance Alert
        Message: "Your company laptop is experiencing high resource utilization. CPU/RAM usage has reached a high level. Please check your system."
        """
        try:
            recipient = target_email or current_app.config.get('MAIL_USERNAME')
            if not recipient:
                logging.warning("No recipient email address configured for performance alert. Skipping email dispatch.")
                return False

            subject = "Laptop Performance Alert"
            body = (
                "Your company laptop is experiencing high resource utilization. "
                "CPU/RAM usage has reached a high level. Please check your system."
            )
            if metric_type and value is not None:
                body += f"\n\n[System Telemetry Details]\nMetric: {metric_type}\nCurrent Usage: {value}%\nConfigured Threshold: {threshold}%"

            # Check if SMTP details are configured
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                logging.info(f"[Mock Mail] Performance alert dispatched to {recipient}. Subject: '{subject}' | Message: '{body}'")
                return True

            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body
            )
            mail.send(msg)
            logging.info(f"Performance alert email successfully sent to {recipient}.")
            return True
        except Exception as e:
            logging.error(f"Failed to dispatch performance alert email to {target_email}: {str(e)}")
            return False

    @staticmethod
    def send_admin_manual_email(target_email, custom_message=None):
        """
        Dispatches manual admin alert to client when Admin clicks 'Send Email' button from Admin Dashboard.
        Subject: Admin Alert – Laptop Issue
        Message: "Hello, we noticed a performance issue with your company laptop. Please check your laptop and take the necessary action."
        """
        try:
            recipient = target_email or current_app.config.get('MAIL_USERNAME')
            if not recipient:
                logging.warning("No recipient email provided for admin alert. Skipping email dispatch.")
                return False

            subject = "Admin Alert – Laptop Issue"
            body = custom_message or (
                "Hello, we noticed a performance issue with your company laptop. "
                "Please check your laptop and take the necessary action."
            )

            # Check if SMTP details are configured
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                logging.info(f"[Mock Mail] Admin manual alert dispatched to {recipient}. Subject: '{subject}' | Message: '{body}'")
                return True

            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body
            )
            mail.send(msg)
            logging.info(f"Admin alert email successfully sent to {recipient}.")
            return True
        except Exception as e:
            logging.error(f"Failed to dispatch admin alert email to {target_email}: {str(e)}")
            return False

    @staticmethod
    def send_alert_email(metric_type, value, threshold, target_email=None):
        """Maintained for backward compatibility with existing code calls."""
        return MailHelper.send_performance_alert(target_email, metric_type, value, threshold)

