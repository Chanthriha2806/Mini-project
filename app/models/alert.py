from datetime import datetime
from app import db

class Alert(db.Model):
    """Breached thresholds alert history table model."""
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    metric_type = db.Column(db.String(20), nullable=False)  # 'CPU', 'RAM', 'DISK'
    message = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Float, nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='ACTIVE')  # 'ACTIVE', 'RESOLVED'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Alert {self.metric_type} ({self.status}) - Val: {self.value}>"
