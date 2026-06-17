"""
Vercel WSGI entry point.
Vercel calls this module and looks for `app` (a WSGI callable).
"""
import os
import traceback

_startup_error = None

try:
    from app import create_app
    app = create_app(os.getenv('FLASK_ENV', 'production'))
except Exception as e:
    _startup_error = traceback.format_exc()

    # Minimal fallback app that reveals the startup error
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def show_error(path):
        return jsonify({
            'error': 'App failed to start',
            'detail': _startup_error
        }), 500
