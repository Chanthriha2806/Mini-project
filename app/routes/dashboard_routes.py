from flask import Blueprint, render_template, jsonify
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
    metrics = DashboardController.get_api_metrics(current_user)
    return jsonify(metrics)

@dashboard_bp.route('/api/charts')
@login_required
def get_chart_history():
    """Endpoint returning historical metric logs mapped for Chart.js rendering."""
    history = DashboardController.get_api_historical_metrics()
    return jsonify(history)

@dashboard_bp.route('/api/alerts/clear', methods=['POST'])
@login_required
def clear_alerts():
    """Endpoint to purge resolved alerts from the database."""
    success, message = DashboardController.clear_resolved_alerts()
    return jsonify({'success': success, 'message': message})

