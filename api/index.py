import os
import sys

# Ensure root workspace directory is in python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Expose WSGI handler for Vercel Serverless Function
app = create_app('production')
