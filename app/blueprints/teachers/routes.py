from flask import render_template, request, jsonify, redirect, url_for, flash
from app.blueprints.teachers import teachers_bp
from app.models.teacher import Teacher
from app.models.attendance import TeacherAttendance
from app.extensions import db
from app.services.performance_analytics import TPDIEngine


@teachers_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    school_id = request.args.get('school_id', type=int)
    category = request.args.get('category', '')

    query = Teacher.query.filter_by(is_active=True)
    if search:
        query = query.filter(
            (Teacher.first_name + ' ' + Teacher.last_name).ilike(f'%{search}%')
        )
    if school_id:
        query = query.filter_by(school_id=school_id)
    if category:
        query = query.filter_by(tpdi_category=category)

    teachers = query.paginate(page=page, per_page=25, error_out=False)
    return render_template('teachers/index.html', teachers=teachers, search=search)


@teachers_bp.route('/<int:teacher_id>')
def detail(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    recent_attendance = (TeacherAttendance.query
                         .filter_by(teacher_id=teacher_id)
                         .order_by(TeacherAttendance.date.desc())
                         .limit(30).all())
    return render_template('teachers/detail.html',
                           teacher=teacher,
                           attendance=recent_attendance)


@teachers_bp.route('/<int:teacher_id>/recalculate-tpdi', methods=['POST'])
def recalculate_tpdi(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    TPDIEngine.calculate(teacher)
    db.session.commit()
    return jsonify({'tpdi_score': teacher.tpdi_score, 'tpdi_category': teacher.tpdi_category})
