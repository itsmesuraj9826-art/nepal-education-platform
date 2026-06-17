from datetime import datetime
from app.extensions import db


class Student(db.Model):
    __tablename__ = 'students'

    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.String(30), unique=True, nullable=False, index=True)
    emis_number     = db.Column(db.String(30), unique=True, index=True)
    first_name      = db.Column(db.String(80), nullable=False)
    last_name       = db.Column(db.String(80), nullable=False)
    gender          = db.Column(db.String(10))
    date_of_birth   = db.Column(db.Date)
    nationality     = db.Column(db.String(30), default='Nepali')
    ethnicity       = db.Column(db.String(50))
    religion        = db.Column(db.String(50))
    photo_url       = db.Column(db.String(255))

    # Guardian
    father_name     = db.Column(db.String(150))
    mother_name     = db.Column(db.String(150))
    guardian_name   = db.Column(db.String(150))
    guardian_phone  = db.Column(db.String(20))
    guardian_email  = db.Column(db.String(120))
    address         = db.Column(db.Text)

    # Current School
    school_id       = db.Column(db.Integer, db.ForeignKey('schools.id'))
    current_grade   = db.Column(db.String(10))
    section         = db.Column(db.String(10))
    roll_number     = db.Column(db.Integer)
    academic_year   = db.Column(db.String(10))

    # AI Risk Scores (updated nightly)
    dropout_risk_score     = db.Column(db.Float, default=0.0)   # 0.0–1.0
    performance_trend      = db.Column(db.String(20))            # improving | stable | declining
    learning_gaps          = db.Column(db.Text)                  # JSON array of subjects/topics

    is_active       = db.Column(db.Boolean, default=True)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    attendance_records = db.relationship('StudentAttendance', backref='student', lazy='dynamic')
    enrollments        = db.relationship('StudentEnrollment', backref='student', lazy='dynamic')
    results            = db.relationship('StudentResult', backref='student', lazy='dynamic')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'full_name': self.full_name,
            'gender': self.gender,
            'school_id': self.school_id,
            'current_grade': self.current_grade,
            'section': self.section,
            'roll_number': self.roll_number,
            'dropout_risk_score': self.dropout_risk_score,
            'performance_trend': self.performance_trend,
            'is_active': self.is_active,
        }

    def __repr__(self):
        return f'<Student {self.student_id}: {self.full_name}>'


class StudentEnrollment(db.Model):
    __tablename__ = 'student_enrollments'

    id            = db.Column(db.Integer, primary_key=True)
    student_id    = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    school_id     = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    grade         = db.Column(db.String(10))
    academic_year = db.Column(db.String(10))
    enrolled_on   = db.Column(db.Date)
    left_on       = db.Column(db.Date)
    left_reason   = db.Column(db.String(150))  # promoted | transferred | dropout | completed
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
