import os
import sys

# Ensure root workspace directory is in python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

try:
    app = create_app('production')
except Exception as e:
    import traceback
    err_tb = traceback.format_exc()
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_fallback():
        return f"<h3>Startup Exception:</h3><pre>{err_tb}</pre>", 200
