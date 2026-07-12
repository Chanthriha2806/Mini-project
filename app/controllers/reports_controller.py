import os
from datetime import datetime, timedelta
from app import db
from app.models.monitoring import MonitoringHistory
from app.models.alert import Alert
from app.models.report import Report
from app.utilities.report_generator import ReportGenerator
from flask import current_app

class ReportsController:
    """Controller to query historical logs data, compute statistical metrics, and coordinate report builds."""

    @staticmethod
    def get_reports_history():
        """Fetches list of generated reports from the database."""
        return Report.query.order_by(Report.created_at.desc()).all()

    @staticmethod
    def generate_report(report_type, file_format):
        """
        Coordinates database queries, computes averages and peaks,
        triggers the appropriate file builder, and records a history entry.
        """
        now = datetime.utcnow()
        range_days = 1
        
        # 1. Resolve timeframe start
        if report_type == 'daily':
            start_date = now - timedelta(days=1)
            range_days = 1
        elif report_type == 'weekly':
            start_date = now - timedelta(days=7)
            range_days = 7
        elif report_type == 'monthly':
            start_date = now - timedelta(days=30)
            range_days = 30
        else:
            return False, "Invalid report type specified."

        # 2. Query aggregate metrics averages and maxes
        # CPU
        cpu_avg = db.session.query(db.func.avg(MonitoringHistory.cpu_usage)).filter(MonitoringHistory.created_at >= start_date).scalar()
        cpu_max = db.session.query(db.func.max(MonitoringHistory.cpu_usage)).filter(MonitoringHistory.created_at >= start_date).scalar()
        
        # Memory
        ram_avg = db.session.query(db.func.avg(MonitoringHistory.ram_usage)).filter(MonitoringHistory.created_at >= start_date).scalar()
        ram_max = db.session.query(db.func.max(MonitoringHistory.ram_usage)).filter(MonitoringHistory.created_at >= start_date).scalar()
        
        # Disk
        disk_avg = db.session.query(db.func.avg(MonitoringHistory.disk_usage)).filter(MonitoringHistory.created_at >= start_date).scalar()
        disk_max = db.session.query(db.func.max(MonitoringHistory.disk_usage)).filter(MonitoringHistory.created_at >= start_date).scalar()
        
        # Network speeds
        up_avg = db.session.query(db.func.avg(MonitoringHistory.upload_speed)).filter(MonitoringHistory.created_at >= start_date).scalar()
        up_max = db.session.query(db.func.max(MonitoringHistory.upload_speed)).filter(MonitoringHistory.created_at >= start_date).scalar()
        down_avg = db.session.query(db.func.avg(MonitoringHistory.download_speed)).filter(MonitoringHistory.created_at >= start_date).scalar()
        down_max = db.session.query(db.func.max(MonitoringHistory.download_speed)).filter(MonitoringHistory.created_at >= start_date).scalar()

        # 3. Compile overview statistics dict
        stats = {
            'cpu_avg': round(cpu_avg or 0.0, 1),
            'cpu_max': round(cpu_max or 0.0, 1),
            'ram_avg': round(ram_avg or 0.0, 1),
            'ram_max': round(ram_max or 0.0, 1),
            'disk_avg': round(disk_avg or 0.0, 1),
            'disk_max': round(disk_max or 0.0, 1),
            'upload_avg': round(up_avg or 0.0, 1),
            'upload_max': round(up_max or 0.0, 1),
            'download_avg': round(down_avg or 0.0, 1),
            'download_max': round(down_max or 0.0, 1),
            'generated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'range_days': range_days
        }

        # 4. Query triggered alerts logs in range
        alerts = Alert.query.filter(Alert.created_at >= start_date).order_by(Alert.created_at.desc()).all()
        alerts_list = []
        for alt in alerts:
            alerts_list.append({
                'timestamp': alt.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'metric_type': alt.metric_type,
                'status': alt.status,
                'message': alt.message,
                'value': alt.value,
                'threshold': alt.threshold
            })

        # 5. Define files path and name schema
        timestamp_str = now.strftime('%Y%m%d_%H%M%S')
        ext = 'pdf' if file_format == 'pdf' else 'xlsx'
        filename = f"report_{report_type}_{timestamp_str}.{ext}"
        
        # Reports directory in static folder
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        filepath = os.path.join(reports_dir, filename)

        # 6. Execute appropriate generator
        try:
            if file_format == 'pdf':
                ReportGenerator.build_pdf(stats, alerts_list, report_type, filepath)
            elif file_format == 'excel':
                ReportGenerator.build_excel(stats, alerts_list, report_type, filepath)
            else:
                return False, "Unsupported file format."

            # Save report log in MySQL database
            db_entry = Report(
                report_type=report_type.upper(),
                file_path=filename
            )
            db.session.add(db_entry)
            db.session.commit()

            return True, filename
        except Exception as e:
            db.session.rollback()
            return False, f"Failed file write operations: {str(e)}"
