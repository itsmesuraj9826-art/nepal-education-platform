import os
from flask import Flask
from config import config_map
from app.extensions import db, migrate, jwt, cors, mail, limiter


def create_app(env_name: str = 'default') -> Flask:
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static',
    )
    app.config.from_object(config_map[env_name])

    # ── Extensions ────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})
    mail.init_app(app)
    limiter.init_app(app)

    # ── Blueprints ────────────────────────────────────────
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.schools import schools_bp
    from app.blueprints.teachers import teachers_bp
    from app.blueprints.students import students_bp
    from app.blueprints.attendance import attendance_bp
    from app.blueprints.exams import exams_bp
    from app.blueprints.api import api_bp

    app.register_blueprint(auth_bp,       url_prefix='/auth')
    app.register_blueprint(dashboard_bp,  url_prefix='/dashboard')
    app.register_blueprint(schools_bp,    url_prefix='/schools')
    app.register_blueprint(teachers_bp,   url_prefix='/teachers')
    app.register_blueprint(students_bp,   url_prefix='/students')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(exams_bp,      url_prefix='/exams')
    app.register_blueprint(api_bp,        url_prefix='/api/v1')

    # ── Root redirect ─────────────────────────────────────
    from flask import redirect, url_for

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # ── Shell context ─────────────────────────────────────
    @app.shell_context_processor
    def make_shell_context():
        from app.models import School, Teacher, Student, User
        return dict(db=db, School=School, Teacher=Teacher, Student=Student, User=User)

    return app
