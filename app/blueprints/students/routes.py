from flask import render_template, request, jsonify
from app.blueprints.students import students_bp
from app.models.student import Student
from app.models.exam import StudentResult


@students_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    school_id = request.args.get('school_id', type=int)
    grade = request.args.get('grade', '')
    risk = request.args.get('risk', '')   # high | medium | low

    query = Student.query.filter_by(is_active=True)
    if search:
        query = query.filter(
            (Student.first_name + ' ' + Student.last_name).ilike(f'%{search}%')
        )
    if school_id:
        query = query.filter_by(school_id=school_id)
    if grade:
        query = query.filter_by(current_grade=grade)
    if risk == 'high':
        query = query.filter(Student.dropout_risk_score >= 0.7)
    elif risk == 'medium':
        query = query.filter(Student.dropout_risk_score.between(0.4, 0.7))
    elif risk == 'low':
        query = query.filter(Student.dropout_risk_score < 0.4)

    students = query.paginate(page=page, per_page=25, error_out=False)
    return render_template('students/index.html', students=students, search=search)


@students_bp.route('/<int:student_id>')
def detail(student_id):
    student = Student.query.get_or_404(student_id)
    results = (StudentResult.query
               .filter_by(student_id=student_id)
               .order_by(StudentResult.created_at.desc())
               .limit(20).all())
    return render_template('students/detail.html', student=student, results=results)
