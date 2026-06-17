"""
Vercel WSGI entry point.
Vercel calls this module and looks for `app` (a WSGI callable).
"""
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'production'))

# Vercel looks for a variable named `app`
# Flask's app object is a valid WSGI callable — nothing else needed.
