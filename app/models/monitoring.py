from datetime import datetime
from app import db

class MonitoringHistory(db.Model):
    """Time-series performance metrics table model."""
    __tablename__ = 'monitoring_history'

    id = db.Column(db.Integer, primary_key=True)
    cpu_usage = db.Column(db.Float, nullable=False)
    ram_usage = db.Column(db.Float, nullable=False)
    disk_usage = db.Column(db.Float, nullable=False)
    upload_speed = db.Column(db.Float, nullable=False)
    download_speed = db.Column(db.Float, nullable=False)
    
    # Metadata for remote monitoring
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    hostname = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('history', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<MonitoringHistory {self.created_at} | CPU: {self.cpu_usage}% | RAM: {self.ram_usage}%>"
