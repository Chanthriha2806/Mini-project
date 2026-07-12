from app import db

class Setting(db.Model):
    """Threshold rules and refresh settings configuration table model."""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    cpu_threshold = db.Column(db.Float, nullable=False, default=90.0)
    ram_threshold = db.Column(db.Float, nullable=False, default=90.0)
    disk_threshold = db.Column(db.Float, nullable=False, default=95.0)
    refresh_interval = db.Column(db.Integer, nullable=False, default=5)
    email_address = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Setting for User ID {self.user_id}>"
