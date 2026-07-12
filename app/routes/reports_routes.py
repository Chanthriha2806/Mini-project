import os
from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required
from app.controllers.reports_controller import ReportsController

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def reports_home():
    """Renders the reports home view containing generation triggers and file logs history."""
    history = ReportsController.get_reports_history()
    return render_template('reports.html', history=history)

@reports_bp.route('/download/<filename>')
@login_required
def download_report(filename):
    """Transfers the target report file to the client for local download."""
    reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
    # Validate existence to prevent errors
    if not os.path.exists(os.path.join(reports_dir, filename)):
        flash("Target report file no longer exists on this server.", "danger")
        return redirect(url_for('reports.reports_home'))
    return send_from_directory(reports_dir, filename, as_attachment=True)

@reports_bp.route('/generate/<report_type>/<file_format>')
@login_required
def generate(report_type, file_format):
    """Triggers telemetry statistics calculations and returns file for download."""
    success, result = ReportsController.generate_report(report_type, file_format)
    if success:
        flash(f"{report_type.capitalize()} report compiled successfully. Starting download...", "success")
        return redirect(url_for('reports.download_report', filename=result))
    else:
        flash(f"Report compilation failed: {result}", "danger")
        return redirect(url_for('reports.reports_home'))
