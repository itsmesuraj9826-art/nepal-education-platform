"""
Nepal National School Monitoring, Teacher Accountability
& Academic Intelligence Platform

PyCharm: right-click app.py > Run 'app'
CLI:     flask run --debug
"""
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True,
    )
