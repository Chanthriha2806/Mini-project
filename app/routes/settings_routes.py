from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.controllers.settings_controller import SettingsController

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/')
@login_required
def settings_home():
    """Renders user threshold rules and refresh schedules configurations view."""
    settings = SettingsController.get_user_settings(current_user.id)
    return render_template('settings.html', settings=settings)

@settings_bp.route('/update', methods=['POST'])
@login_required
def update_settings():
    """Validates form parameters and updates database configurations."""
    cpu_threshold = request.form.get('cpu_threshold')
    ram_threshold = request.form.get('ram_threshold')
    disk_threshold = request.form.get('disk_threshold')
    refresh_interval = request.form.get('refresh_interval')
    email_address = request.form.get('email_address', '')

    success, message = SettingsController.update_user_settings(
        current_user, cpu_threshold, ram_threshold, disk_threshold, refresh_interval, email_address
    )
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect(url_for('settings.settings_home'))
