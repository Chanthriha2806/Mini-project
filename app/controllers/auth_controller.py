from app import db
from app.models.user import User
from app.models.setting import Setting
from flask import current_app
from flask_login import login_user, logout_user

class AuthController:
    """Controller logic for user registration, authentication, logout, and profile updates."""

    @staticmethod
    def register_user(username, email, password):
        """
        Registers a new user in the database.
        Automatically provisions default monitoring settings for the user.
        """
        # Validate unique fields
        if User.query.filter_by(username=username).first():
            return False, "Username is already taken."
        if User.query.filter_by(email=email).first():
            return False, "Email address is already registered."

        try:
            # Create user
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()  # Populates user ID before commit

            # Create default monitor settings
            default_settings = Setting(
                user_id=new_user.id,
                cpu_threshold=current_app.config.get('DEFAULT_CPU_THRESHOLD', 90.0),
                ram_threshold=current_app.config.get('DEFAULT_RAM_THRESHOLD', 90.0),
                disk_threshold=current_app.config.get('DEFAULT_DISK_THRESHOLD', 95.0),
                refresh_interval=current_app.config.get('DEFAULT_REFRESH_INTERVAL', 5),
                email_address=email
            )
            db.session.add(default_settings)
            db.session.commit()
            return True, "Registration successful. You can now login!"
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed due to a database error: {str(e)}"

    @staticmethod
    def login_user_session(email_or_username, password, remember_me=False):
        """
        Authenticates user by email or username, verifying password hashes.
        Starts session if credentials match.
        """
        # Lookup user by email or username
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()
        if not user or not user.check_password(password):
            return False, "Invalid username/email or password."

        login_user(user, remember=remember_me)
        return True, "Login successful!"

    @staticmethod
    def logout_user_session():
        """Terminates active session."""
        logout_user()
        return True, "Logged out successfully."

    @staticmethod
    def update_profile_info(user, username, email, current_password=None, new_password=None):
        """
        Updates profile username, email, and password.
        Performs identity verification via current password.
        """
        # If credentials change, verify current password
        if new_password:
            if not current_password or not user.check_password(current_password):
                return False, "Incorrect current password verification."

        # Verify uniqueness if fields changed
        if username != user.username:
            if User.query.filter(User.username == username, User.id != user.id).first():
                return False, "Username is already in use."
            user.username = username

        if email != user.email:
            if User.query.filter(User.email == email, User.id != user.id).first():
                return False, "Email address is already in use."
            user.email = email

        if new_password:
            user.set_password(new_password)

        try:
            db.session.commit()
            return True, "Profile details updated successfully."
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update profile: {str(e)}"
