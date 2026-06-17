from datetime import datetime
from app.extensions import db


class Province(db.Model):
    __tablename__ = 'provinces'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_np = db.Column(db.String(100))
    code = db.Column(db.String(10))
    districts = db.relationship('District', backref='province', lazy='dynamic')


class District(db.Model):
    __tablename__ = 'districts'
    id          = db.Column(db.Integer, primary_key=True)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    name_np     = db.Column(db.String(100))
    code        = db.Column(db.String(10))
    municipalities = db.relationship('Municipality', backref='district', lazy='dynamic')


class Municipality(db.Model):
    __tablename__ = 'municipalities'
    id          = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    name        = db.Column(db.String(150), nullable=False)
    name_np     = db.Column(db.String(150))
    mun_type    = db.Column(db.String(30))   # Metropolitan | Sub-Metropolitan | Municipality | Rural Municipality
    code        = db.Column(db.String(10))
    schools = db.relationship('School', backref='municipality', lazy='dynamic')


class School(db.Model):
    __tablename__ = 'schools'

    id              = db.Column(db.Integer, primary_key=True)
    school_code     = db.Column(db.String(20), unique=True, nullable=False, index=True)
    emis_id         = db.Column(db.String(30), unique=True, index=True)
    name_en         = db.Column(db.String(255), nullable=False)
    name_np         = db.Column(db.String(255))

    # Classification
    school_type     = db.Column(db.String(50))   # Government | Community | Institutional
    school_level    = db.Column(db.String(50))   # Primary | Lower Secondary | Secondary | Higher Secondary
    academic_streams = db.Column(db.Text)        # JSON array of streams

    # Location
    province_id     = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    district_id     = db.Column(db.Integer, db.ForeignKey('districts.id'))
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipalities.id'))
    ward_number     = db.Column(db.Integer)
    address         = db.Column(db.Text)
    latitude        = db.Column(db.Float)
    longitude       = db.Column(db.Float)

    # Contact
    phone           = db.Column(db.String(20))
    email           = db.Column(db.String(120))
    website         = db.Column(db.String(200))

    # Staff & Students
    principal_name  = db.Column(db.String(150))
    num_teachers    = db.Column(db.Integer, default=0)
    num_students    = db.Column(db.Integer, default=0)

    # Status
    status          = db.Column(db.String(20), default='active')   # active | inactive | closed
    established_year = db.Column(db.Integer)

    # Sync metadata
    last_synced_at  = db.Column(db.DateTime)
    data_source     = db.Column(db.String(50))   # emis | manual | import
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teachers  = db.relationship('Teacher', backref='school', lazy='dynamic')
    students  = db.relationship('Student', backref='school', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'school_code': self.school_code,
            'emis_id': self.emis_id,
            'name_en': self.name_en,
            'name_np': self.name_np,
            'school_type': self.school_type,
            'school_level': self.school_level,
            'ward_number': self.ward_number,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'email': self.email,
            'principal_name': self.principal_name,
            'num_teachers': self.num_teachers,
            'num_students': self.num_students,
            'status': self.status,
        }

    def __repr__(self):
        return f'<School {self.school_code}: {self.name_en}>'
