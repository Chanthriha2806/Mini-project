import os
import webbrowser
import threading
import time
from app import create_app

# Resolve environment mode
env_mode = os.environ.get('FLASK_ENV')
if not env_mode:
    env_mode = 'production' if os.environ.get('VERCEL') == '1' else 'development'

# Create flask application instance
app = create_app(env_mode)

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

    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))

