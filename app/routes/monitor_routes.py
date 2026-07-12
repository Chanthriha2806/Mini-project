from flask import Blueprint, render_template
from flask_login import login_required
from app.controllers.monitor_controller import MonitorController

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/')
@login_required
def index():
    """Renders the detailed system specifications monitoring page."""
    specs_data = MonitorController.get_detailed_system_specs()
    return render_template('monitor.html', **specs_data)
