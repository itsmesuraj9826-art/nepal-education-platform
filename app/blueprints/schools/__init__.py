from flask import Blueprint
schools_bp = Blueprint('schools', __name__)
from app.blueprints.schools import routes  # noqa
