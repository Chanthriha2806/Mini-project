from app import db
from app.models.user import User
from app.models.setting import Setting
from app.models.alert import Alert
from app.models.monitoring import MonitoringHistory
from app.models.report import Report
from app.models.ticket import Ticket

# Expose models for imports throughout the application package
__all__ = ['db', 'User', 'Setting', 'Alert', 'MonitoringHistory', 'Report', 'Ticket']

