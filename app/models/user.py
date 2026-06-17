from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name     = db.Column(db.String(150))
    phone         = db.Column(db.String(20))

    # Role hierarchy: federal | provincial | district | municipality | principal | teacher
    role          = db.Column(db.String(30), nullable=False, default='teacher')
    province_id   = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=True)
    district_id   = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipalities.id'), nullable=True)
    school_id     = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)

    is_active     = db.Column(db.Boolean, default=True)
    last_login    = db.Column(db.DateTime)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
        }

    def __repr__(self):
        return f'<User {self.username} [{self.role}]>'
