from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Renders the primary real-time monitoring dashboard template."""
    dashboard_data = DashboardController.get_dashboard_data(current_user)
    return render_template('dashboard.html', **dashboard_data)

@dashboard_bp.route('/api/metrics')
@login_required
def get_metrics():
    """Endpoint returning latest live server telemetry measurements."""
    user_id = request.args.get('user_id', type=int)
    hostname = request.args.get('hostname', type=str)
    metrics = DashboardController.get_api_metrics(current_user, user_id=user_id, hostname=hostname)
    return jsonify(metrics)

@dashboard_bp.route('/api/charts')
@login_required
def get_chart_history():
    """Endpoint returning historical metric logs mapped for Chart.js rendering."""
    user_id = request.args.get('user_id', type=int)
    hostname = request.args.get('hostname', type=str)
    history = DashboardController.get_api_historical_metrics(current_user, user_id=user_id, hostname=hostname)
    return jsonify(history)

@dashboard_bp.route('/api/metrics/report', methods=['POST'])
@login_required
def report_metrics():
    """Endpoint for client agents to report CPU, RAM, Disk, and Network telemetry."""
    data = request.get_json() or {}
    success, message = DashboardController.save_client_metrics(current_user, data, request.remote_addr)
    return jsonify({'success': success, 'message': message}), 200 if success else 400

@dashboard_bp.route('/api/alerts/clear', methods=['POST'])
@login_required
def clear_alerts():
    """Endpoint to purge resolved alerts from the database."""
    success, message = DashboardController.clear_resolved_alerts()
    return jsonify({'success': success, 'message': message})

