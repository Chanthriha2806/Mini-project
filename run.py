import os
from app import create_app

# Create flask application instance
app = create_app('production')

if __name__ == '__main__':
    import webbrowser
    import threading
    import time

    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        def launch_browser(p):
            time.sleep(1.5)
            webbrowser.open(f"http://127.0.0.1:{p}")
        threading.Thread(target=launch_browser, args=(port,), daemon=True).start()

    app.run(host='0.0.0.0', port=port, debug=False)
