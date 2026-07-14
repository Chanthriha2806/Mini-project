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

@dashboard_bp.route('/api/process/kill', methods=['POST'])
@login_required
def kill_process():
    """Endpoint for administrators to terminate runaway CPU/RAM tasks."""
    data = request.get_json() or {}
    pid = data.get('pid')
    if not pid:
        return jsonify({'success': False, 'message': 'Missing process PID.'}), 400
    success, message = DashboardController.kill_process(current_user, pid)
    return jsonify({'success': success, 'message': message}), 200 if success else 400

@dashboard_bp.route('/api/ai/chat', methods=['POST'])
@login_required
def chat_with_ai():
    """Endpoint for context-aware diagnostic recommendations chat."""
    data = request.get_json() or {}
    message = data.get('message')
    metrics_context = data.get('metrics')
    if not message:
        return jsonify({'success': False, 'message': 'Missing query message.'}), 400
    
    # If no metrics context was supplied from frontend, query it fresh
    if not metrics_context:
        user_id = data.get('user_id')
        hostname = data.get('hostname')
        metrics_context = DashboardController.get_api_metrics(current_user, user_id=user_id, hostname=hostname)
        
    response_md = DashboardController.chat_with_ai(current_user, message, metrics_context)
    return jsonify({'success': True, 'response': response_md})


