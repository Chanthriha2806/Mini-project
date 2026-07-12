from datetime import datetime
from app import db

class Report(db.Model):
    """System statistics PDF/Excel reports metadata table model."""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(20), nullable=False)  # 'DAILY', 'WEEKLY', 'MONTHLY'
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Report {self.report_type} created at {self.created_at}>"
