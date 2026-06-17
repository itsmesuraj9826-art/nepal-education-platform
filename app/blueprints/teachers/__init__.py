from flask import Blueprint
teachers_bp = Blueprint('teachers', __name__)
from app.blueprints.teachers import routes  # noqa
