from datetime import datetime
from app.extensions import db


class Exam(db.Model):
    __tablename__ = 'exams'

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(255), nullable=False)
    subject         = db.Column(db.String(100), nullable=False)
    grade           = db.Column(db.String(10), nullable=False)
    academic_year   = db.Column(db.String(10))
    exam_type       = db.Column(db.String(50))   # terminal | unit | final | mock | weekly
    difficulty      = db.Column(db.String(20))   # easy | medium | hard | mixed
    total_marks     = db.Column(db.Integer, default=100)
    pass_marks      = db.Column(db.Integer, default=40)
    duration_minutes = db.Column(db.Integer, default=180)
    exam_date       = db.Column(db.Date)
    school_id       = db.Column(db.Integer, db.ForeignKey('schools.id'))
    created_by      = db.Column(db.Integer, db.ForeignKey('users.id'))
    ai_generated    = db.Column(db.Boolean, default=False)
    curriculum_src  = db.Column(db.Text)         # JSON list of source PDF paths
    status          = db.Column(db.String(20), default='draft')
    # draft | published | completed | cancelled
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    questions = db.relationship('Question', backref='exam', lazy='dynamic', cascade='all, delete-orphan')
    papers    = db.relationship('ExamPaper', backref='exam', lazy='dynamic')
    results   = db.relationship('StudentResult', backref='exam', lazy='dynamic')


class Question(db.Model):
    __tablename__ = 'questions'

    id              = db.Column(db.Integer, primary_key=True)
    exam_id         = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_no     = db.Column(db.Integer)
    question_type   = db.Column(db.String(30))
    # mcq | true_false | fill_blank | short_answer | long_answer | practical | critical_thinking
    question_text   = db.Column(db.Text, nullable=False)
    options         = db.Column(db.Text)   # JSON for MCQ options
    correct_answer  = db.Column(db.Text)
    marks           = db.Column(db.Float, default=1.0)
    difficulty      = db.Column(db.String(20))
    chapter         = db.Column(db.String(150))
    topic           = db.Column(db.String(150))
    bloom_level     = db.Column(db.String(30))  # remember | understand | apply | analyze | evaluate | create
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)


class ExamPaper(db.Model):
    __tablename__ = 'exam_papers'

    id          = db.Column(db.Integer, primary_key=True)
    exam_id     = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    paper_url   = db.Column(db.String(255))
    answer_key_url = db.Column(db.String(255))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentResult(db.Model):
    __tablename__ = 'student_results'

    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    exam_id         = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)
    school_id       = db.Column(db.Integer, db.ForeignKey('schools.id'))
    marks_obtained  = db.Column(db.Float)
    total_marks     = db.Column(db.Float)
    percentage      = db.Column(db.Float)
    grade           = db.Column(db.String(5))   # A+ A B+ B C+ C D E
    rank_in_class   = db.Column(db.Integer)
    ai_evaluated    = db.Column(db.Boolean, default=False)
    evaluator_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    remarks         = db.Column(db.Text)
    subject_breakdown = db.Column(db.Text)  # JSON of per-question marks
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    answer_sheet = db.relationship('AnswerSheet', backref='result', uselist=False)


class AnswerSheet(db.Model):
    __tablename__ = 'answer_sheets'

    id              = db.Column(db.Integer, primary_key=True)
    result_id       = db.Column(db.Integer, db.ForeignKey('student_results.id'), nullable=False)
    image_urls      = db.Column(db.Text)     # JSON list of scanned page URLs
    ocr_text        = db.Column(db.Text)     # raw OCR output
    ai_marks_json   = db.Column(db.Text)     # per-question AI marks
    ocr_confidence  = db.Column(db.Float)
    processed_at    = db.Column(db.DateTime)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
