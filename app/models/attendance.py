from datetime import datetime
from app.extensions import db


class TeacherAttendance(db.Model):
    __tablename__ = 'teacher_attendance'

    id              = db.Column(db.Integer, primary_key=True)
    teacher_id      = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False, index=True)
    school_id       = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    date            = db.Column(db.Date, nullable=False, index=True)
    check_in_time   = db.Column(db.Time)
    check_out_time  = db.Column(db.Time)
    status          = db.Column(db.String(20), default='present')
    # present | absent | late | half_day | leave | holiday | weekend

    # Verification method
    method          = db.Column(db.String(20))
    # gps | face | mobile_app | web | manual

    # GPS data
    check_in_lat    = db.Column(db.Float)
    check_in_lon    = db.Column(db.Float)
    check_out_lat   = db.Column(db.Float)
    check_out_lon   = db.Column(db.Float)
    geo_valid       = db.Column(db.Boolean, default=True)

    # AI fraud flags
    fraud_flag      = db.Column(db.Boolean, default=False)
    fraud_reason    = db.Column(db.String(255))
    fraud_score     = db.Column(db.Float, default=0.0)   # 0–1

    # Photo evidence
    check_in_photo  = db.Column(db.String(255))
    face_match_score = db.Column(db.Float)

    notes           = db.Column(db.Text)
    recorded_by     = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('teacher_id', 'date', name='uq_teacher_date'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'date': str(self.date),
            'check_in_time': str(self.check_in_time) if self.check_in_time else None,
            'check_out_time': str(self.check_out_time) if self.check_out_time else None,
            'status': self.status,
            'method': self.method,
            'geo_valid': self.geo_valid,
            'fraud_flag': self.fraud_flag,
            'fraud_score': self.fraud_score,
        }


class StudentAttendance(db.Model):
    __tablename__ = 'student_attendance'

    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    school_id   = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    date        = db.Column(db.Date, nullable=False, index=True)
    status      = db.Column(db.String(20), default='present')
    # present | absent | late | leave | holiday
    reason      = db.Column(db.String(255))
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'date', name='uq_student_date'),
    )
