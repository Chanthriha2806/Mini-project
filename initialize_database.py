from app import create_app, db
from app.models.user import User
from app.models.setting import Setting

app = create_app()
with app.app_context():
    db.create_all()
    
    # Create admin user if not exists
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", email="admin@monitor.com", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        
        # Seed settings for admin
        admin_setting = Setting(
            user_id=admin.id,
            cpu_threshold=90.0,
            ram_threshold=90.0,
            disk_threshold=95.0,
            refresh_interval=5,
            email_address="admin@monitor.com"
        )
        db.session.add(admin_setting)
        db.session.commit()

    # Create client user if not exists
    if not User.query.filter_by(username="client").first():
        client = User(username="client", email="client@monitor.com", is_admin=False)
        client.set_password("client123")
        db.session.add(client)
        db.session.commit()
        
        # Seed settings for client
        client_setting = Setting(
            user_id=client.id,
            cpu_threshold=90.0,
            ram_threshold=90.0,
            disk_threshold=95.0,
            refresh_interval=5,
            email_address="client@monitor.com"
        )
        db.session.add(client_setting)
        db.session.commit()

    print("[+] Database initialized and seeded successfully!")
    print("    - Admin credentials: admin / admin123")
    print("    - Client credentials: client / client123")
