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

@settings_bp.route('/test-email', methods=['POST'])
@login_required
def test_email():
    """Endpoint to trigger a test alert email notification."""
    email_address = request.form.get('email_address') or (request.json.get('email_address') if request.is_json else '')
    success, message = SettingsController.send_test_email(current_user, email_address)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from flask import jsonify
        return jsonify({'success': success, 'message': message}), 200 if success else 400

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('settings.settings_home'))

