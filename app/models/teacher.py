from datetime import datetime
from app.extensions import db


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id                  = db.Column(db.Integer, primary_key=True)
    teacher_id          = db.Column(db.String(30), unique=True, nullable=False, index=True)
    govt_employee_no    = db.Column(db.String(30), unique=True, index=True)
    first_name          = db.Column(db.String(80), nullable=False)
    last_name           = db.Column(db.String(80), nullable=False)
    gender              = db.Column(db.String(10))
    date_of_birth       = db.Column(db.Date)
    citizenship_no      = db.Column(db.String(30))
    photo_url           = db.Column(db.String(255))
    face_encoding       = db.Column(db.Text)      # JSON-encoded face embedding for recognition

    # Contact
    phone               = db.Column(db.String(20))
    email               = db.Column(db.String(120))
    permanent_address   = db.Column(db.Text)
    temporary_address   = db.Column(db.Text)

    # Professional
    subject_specialization = db.Column(db.String(150))
    highest_qualification  = db.Column(db.String(100))
    university             = db.Column(db.String(150))
    teaching_license_no    = db.Column(db.String(50))
    service_start_date     = db.Column(db.Date)
    service_type           = db.Column(db.String(30))   # permanent | temporary | contract

    # Current Assignment
    school_id              = db.Column(db.Integer, db.ForeignKey('schools.id'))
    designation            = db.Column(db.String(80))

    # Performance Index (updated by AI engine)
    tpdi_score             = db.Column(db.Float, default=0.0)   # 0–100
    tpdi_category          = db.Column(db.String(30))           # Outstanding | Excellent | Good | Satisfactory | Improvement Required
    attendance_score       = db.Column(db.Float, default=0.0)
    punctuality_score      = db.Column(db.Float, default=0.0)
    student_performance_score = db.Column(db.Float, default=0.0)

    is_active              = db.Column(db.Boolean, default=True)
    created_at             = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at             = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    attendance_records  = db.relationship('TeacherAttendance', backref='teacher', lazy='dynamic')
    transfer_history    = db.relationship('TeacherTransfer', backref='teacher', lazy='dynamic')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'full_name': self.full_name,
            'gender': self.gender,
            'subject_specialization': self.subject_specialization,
            'highest_qualification': self.highest_qualification,
            'school_id': self.school_id,
            'designation': self.designation,
            'tpdi_score': self.tpdi_score,
            'tpdi_category': self.tpdi_category,
            'is_active': self.is_active,
        }

    def __repr__(self):
        return f'<Teacher {self.teacher_id}: {self.full_name}>'


class TeacherTransfer(db.Model):
    __tablename__ = 'teacher_transfers'

    id              = db.Column(db.Integer, primary_key=True)
    teacher_id      = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    from_school_id  = db.Column(db.Integer, db.ForeignKey('schools.id'))
    to_school_id    = db.Column(db.Integer, db.ForeignKey('schools.id'))
    transfer_date   = db.Column(db.Date)
    reason          = db.Column(db.Text)
    order_no        = db.Column(db.String(50))
    approved_by     = db.Column(db.String(150))
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
