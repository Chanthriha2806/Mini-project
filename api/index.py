import os
import sys

# Ensure root workspace directory is in python search path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import create_app

app = create_app('production')

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    return f"<h3>Application Error on Vercel:</h3><pre>{traceback.format_exc()}</pre>", 500

handler = app
