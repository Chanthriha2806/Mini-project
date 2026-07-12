import unittest
from flask import Flask
from app import create_app, db
from app.utilities.system_monitor import SystemMonitor
from app.utilities.ai_engine import RecommendationEngine

class TestITMonitoring(unittest.TestCase):
    """Unit test cases for system monitoring diagnostics, AI recommendations, and route registration."""

    def setUp(self):
        """Prepares a test client configured with in-memory SQLite database to run isolated unit tests."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Build database tables in sqlite memory space
        db.create_all()

    def tearDown(self):
        """Cleans up the database and pops context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_system_metrics_structure(self):
        """Verifies that the SystemMonitor utility consolidates metrics maps containing expected keys."""
        metrics = SystemMonitor.get_system_metrics()
        
        # Check high-level sections exist
        self.assertIn('cpu', metrics)
        self.assertIn('memory', metrics)
        self.assertIn('disk', metrics)
        self.assertIn('network', metrics)
        self.assertIn('system', metrics)
        self.assertIn('active_counts', metrics)

        # Check cpu details keys
        self.assertIn('usage', metrics['cpu'])
        self.assertIn('cores', metrics['cpu'])
        self.assertIn('frequency', metrics['cpu'])

        # Check memory details keys
        self.assertIn('total', metrics['memory'])
        self.assertIn('used', metrics['memory'])
        self.assertIn('percent', metrics['memory'])

        # Check network speed values are numeric
        self.assertIsInstance(metrics['network']['upload_speed'], (int, float))
        self.assertIsInstance(metrics['network']['download_speed'], (int, float))

    def test_ai_recommendation_rules(self):
        """Validates AI recommendation checklist selections based on custom telemetry triggers."""
        # 1. Test CPU critical load rule (>90%)
        recs_cpu = RecommendationEngine.generate_recommendations(
            cpu=95.0, ram=40.0, disk=50.0, upload_speed=0.0, download_speed=0.0, health_status='CRITICAL'
        )
        has_cpu_rec = any(r['metric'] == 'CPU' and r['level'] == 'danger' for r in recs_cpu)
        self.assertTrue(has_cpu_rec, "AI Engine should trigger a Critical CPU recommendation if usage > 90%.")

        # 2. Test RAM critical load rule (>90%)
        recs_ram = RecommendationEngine.generate_recommendations(
            cpu=40.0, ram=92.0, disk=50.0, upload_speed=0.0, download_speed=0.0, health_status='CRITICAL'
        )
        has_ram_rec = any(r['metric'] == 'RAM' and r['level'] == 'danger' for r in recs_ram)
        self.assertTrue(has_ram_rec, "AI Engine should trigger a Critical RAM recommendation if usage > 90%.")

        # 3. Test Disk critical load rule (>95%)
        recs_disk = RecommendationEngine.generate_recommendations(
            cpu=40.0, ram=40.0, disk=98.0, upload_speed=0.0, download_speed=0.0, health_status='CRITICAL'
        )
        has_disk_rec = any(r['metric'] == 'DISK' and r['level'] == 'danger' for r in recs_disk)
        self.assertTrue(has_disk_rec, "AI Engine should trigger a Critical Disk recommendation if usage > 95%.")

        # 4. Test Healthy rule
        recs_healthy = RecommendationEngine.generate_recommendations(
            cpu=30.0, ram=40.0, disk=50.0, upload_speed=100.0, download_speed=100.0, health_status='HEALTHY'
        )
        has_healthy = any(r['level'] == 'success' and 'All Systems Operational' in r['title'] for r in recs_healthy)
        self.assertTrue(has_healthy, "AI Engine should declare all systems operational under healthy conditions.")

    def test_flask_app_initialization(self):
        """Validates that routes and layouts serve HTTP endpoints correctly in test client context."""
        # 1. Login page route responds cleanly
        response_login = self.client.get('/auth/login')
        self.assertEqual(response_login.status_code, 200)
        self.assertIn(b'Login', response_login.data)

        # 2. Register page route responds cleanly
        response_register = self.client.get('/auth/register')
        self.assertEqual(response_register.status_code, 200)
        self.assertIn(b'Register', response_register.data)

        # 3. Protected page (like dashboard index /) redirects to login because guest is not authenticated
        response_dashboard = self.client.get('/')
        self.assertEqual(response_dashboard.status_code, 302)
        self.assertIn('/auth/login', response_dashboard.location)

if __name__ == '__main__':
    unittest.main()
