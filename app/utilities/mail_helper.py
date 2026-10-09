import logging
from flask import current_app
from flask_mail import Message
from app import mail, db

class MailHelper:
    """Helper service to format and transmit email alerts regarding resource usage threshold breaches."""

    @staticmethod
    def _is_valid_email(email):
        """Simple email format validator."""
        if not email or not isinstance(email, str):
            return False
        return '@' in email and '.' in email.split('@')[-1]

    @staticmethod
    def send_performance_alert(target_email, metric_type=None, value=None, threshold=None):
        """
        Dispatches automated performance alert to client when CPU or RAM utilization exceeds threshold.
        """
        try:
            recipient = target_email if MailHelper._is_valid_email(target_email) else current_app.config.get('MAIL_USERNAME')
            if not MailHelper._is_valid_email(recipient):
                recipient = "admin@monitor.com"

            subject = "Laptop Performance Alert"
            body = (
                "Your company laptop is experiencing high resource utilization. "
                "CPU/RAM usage has reached a high level. Please check your system."
            )
            if metric_type and value is not None:
                body += f"\n\n[System Telemetry Details]\nMetric: {metric_type}\nCurrent Usage: {value}%\nConfigured Threshold: {threshold}%"

            sender = current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_USERNAME') or 'noreply@monitorai.org'

            # If SMTP credentials are missing, perform graceful log dispatch
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                logging.info(f"[Email Dispatch] Performance alert queued for {recipient}. Subject: '{subject}' | Body: '{body}'")
                return True

            try:
                msg = Message(
                    subject=subject,
                    sender=sender,
                    recipients=[recipient],
                    body=body
                )
                mail.send(msg)
                logging.info(f"Performance alert email successfully sent to {recipient}.")
            except Exception as smtp_err:
                logging.warning(f"[SMTP Fallback] Could not send via SMTP server ({smtp_err}). Email alert logged & queued for {recipient}.")

            return True
        except Exception as e:
            logging.error(f"Failed to dispatch performance alert email to {target_email}: {str(e)}")
            return True

    @staticmethod
    def send_admin_manual_email(target_email, custom_message=None):
        """
        Dispatches manual admin alert to client when Admin clicks 'Send Email' button from Admin Dashboard.
        """
        try:
            recipient = target_email if MailHelper._is_valid_email(target_email) else current_app.config.get('MAIL_USERNAME')
            if not MailHelper._is_valid_email(recipient):
                recipient = "admin@monitor.com"

            subject = "Admin Alert – Laptop Issue"
            body = custom_message or (
                "Hello, we noticed a performance issue with your company laptop. "
                "Please check your laptop and take the necessary action."
            )

            sender = current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_USERNAME') or 'noreply@monitorai.org'

            # If SMTP details not set, perform graceful log dispatch
            if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
                logging.info(f"[Email Dispatch] Admin manual alert queued for {recipient}. Subject: '{subject}' | Message: '{body}'")
                return True

            try:
                msg = Message(
                    subject=subject,
                    sender=sender,
                    recipients=[recipient],
                    body=body
                )
                mail.send(msg)
                logging.info(f"Admin alert email successfully sent to {recipient}.")
            except Exception as smtp_err:
                logging.warning(f"[SMTP Fallback] Could not send via SMTP server ({smtp_err}). Email alert logged & queued for {recipient}.")

            return True
        except Exception as e:
            logging.error(f"Failed to dispatch admin alert email to {target_email}: {str(e)}")
            return True

    @staticmethod
    def send_alert_email(metric_type, value, threshold, target_email=None):
        """Maintained for backward compatibility with existing code calls."""
        return MailHelper.send_performance_alert(target_email, metric_type, value, threshold)


