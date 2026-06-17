"""
Vercel WSGI entry point.
"""
import os
import traceback

_startup_error = None

try:
    from app import create_app
    _flask_app = create_app(os.getenv('FLASK_ENV', 'production'))

    # Add a global error handler to expose tracebacks
    @_flask_app.errorhandler(Exception)
    def handle_exception(e):
        from flask import jsonify
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

    app = _flask_app

except Exception as e:
    _startup_error = traceback.format_exc()
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def show_error(path):
        return jsonify({'startup_error': _startup_error}), 500
