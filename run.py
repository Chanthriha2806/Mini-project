import os
import webbrowser
import threading
import time
from app import create_app

# Create flask application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

def launch_browser(port):
    """Waits for the server boot-up and opens the default web browser."""
    time.sleep(1.5)
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == '__main__':
    # Use standard dev port 5000 or from environment
    port = int(os.environ.get('PORT', 5000))
    
    # Only open browser once (prevents double launch under Flask debugger reloading)
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Thread(target=launch_browser, args=(port,), daemon=True).start()

    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', True))

