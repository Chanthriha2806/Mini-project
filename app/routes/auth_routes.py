from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User account registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html')

        success, message = AuthController.register_user(username, email, password)
        if success:
            flash(message, "success")
            return redirect(url_for('auth.login'))
        else:
            flash(message, "danger")

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login authentication route."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email_or_username = request.form.get('username_email', '').strip()
        password = request.form.get('password', '')
        remember = 'remember' in request.form

        if not email_or_username or not password:
            flash("Both credentials are required.", "danger")
            return render_template('auth/login.html')

        success, message = AuthController.login_user_session(email_or_username, password, remember)
        if success:
            flash(message, "success")
            # Redirect to next parameter or dashboard
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard.index'))
        else:
            flash(message, "danger")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Ends user session and redirects to login."""
    AuthController.logout_user_session()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Renders profile and processes updates."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        current_pw = request.form.get('current_password', '')
        new_pw = request.form.get('new_password', '')
        confirm_pw = request.form.get('confirm_new_password', '')

        if not username or not email:
            flash("Username and Email are required fields.", "danger")
            return render_template('profile.html')

        if new_pw or current_pw:
            if new_pw != confirm_pw:
                flash("New passwords do not match.", "danger")
                return render_template('profile.html')
            if not current_pw:
                flash("Current password must be provided to save new password.", "danger")
                return render_template('profile.html')

        success, message = AuthController.update_profile_info(
            current_user, username, email, current_pw, new_pw
        )
        if success:
            flash(message, "success")
            return redirect(url_for('auth.profile'))
        else:
            flash(message, "danger")

    return render_template('profile.html')
