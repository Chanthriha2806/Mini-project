from datetime import datetime
from app import db

class Ticket(db.Model):
    """Support and issue ticket table model."""
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')  # 'Open', 'In Progress', 'Resolved', 'Closed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('tickets', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<Ticket #{self.id} '{self.subject}' ({self.status})>"
