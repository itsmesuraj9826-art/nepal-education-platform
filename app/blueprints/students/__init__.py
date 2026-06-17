from flask import Blueprint
students_bp = Blueprint('students', __name__)
from app.blueprints.students import routes  # noqa
