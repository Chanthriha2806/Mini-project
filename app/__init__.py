from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config_by_name

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

import os
import sys

def create_app(config_name='default'):
    """Application Factory pattern for Flask app creation."""
    # Detect if running as a compiled standalone executable (PyInstaller)
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'app', 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'app', 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    else:
        app = Flask(__name__)
        
    app.config.from_object(config_by_name[config_name])


    # Bind extensions to app
    db.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    mail.init_app(app)

    # Import models to ensure registration on Metadata
    from app.models.user import User
    from app.models.setting import Setting
    from app.models.alert import Alert
    from app.models.monitoring import MonitoringHistory
    from app.models.report import Report

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Attempt to auto-create tables on startup
    with app.app_context():
        try:
            db.create_all()
            
            # Auto-seed default credentials if users are empty
            from app.models.user import User
            from app.models.setting import Setting
            
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", email="admin@monitor.com", is_admin=True)
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                
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
                
            if not User.query.filter_by(username="client").first():
                client = User(username="client", email="client@monitor.com", is_admin=False)
                client.set_password("client123")
                db.session.add(client)
                db.session.commit()
                
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
        except Exception as e:
            app.logger.warning(f"Could not connect to database or seed on startup: {e}")


    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.reports_routes import reports_bp
    from app.routes.settings_routes import settings_bp
    from app.routes.monitor_routes import monitor_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(monitor_bp, url_prefix='/monitor')

    return app
