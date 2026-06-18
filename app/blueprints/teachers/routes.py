from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app.blueprints.teachers import teachers_bp
from app.models.teacher import Teacher
from app.models.attendance import TeacherAttendance
from app.extensions import db
from app.services.performance_analytics import TPDIEngine
import uuid


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


@teachers_bp.route('/add', methods=['GET', 'POST'])
def add():
    """School adds a teacher manually."""
    school_id = session.get('school_id')
    if not school_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        if not first_name or not last_name:
            flash('First and last name are required.', 'danger')
            return redirect(url_for('teachers.add'))

        # Auto-generate a unique teacher_id
        teacher_id = f"T-{school_id}-{uuid.uuid4().hex[:6].upper()}"

        teacher = Teacher(
            teacher_id            = teacher_id,
            first_name            = first_name,
            last_name             = last_name,
            gender                = request.form.get('gender', ''),
            phone                 = request.form.get('phone', '').strip(),
            email                 = request.form.get('email', '').strip(),
            subject_specialization= request.form.get('subject', '').strip(),
            highest_qualification = request.form.get('qualification', '').strip(),
            designation           = request.form.get('designation', 'Teacher'),
            service_type          = request.form.get('service_type', 'permanent'),
            school_id             = school_id,
            is_active             = True,
        )
        db.session.add(teacher)

        # update school teacher count
        from app.models.school import School
        school = School.query.get(school_id)
        if school:
            school.num_teachers = Teacher.query.filter_by(school_id=school_id, is_active=True).count() + 1
        db.session.commit()

        flash(f'Teacher {first_name} {last_name} added successfully.', 'success')
        return redirect(url_for('dashboard.school'))

    return render_template('teachers/add.html')


@teachers_bp.route('/<int:teacher_id>/recalculate-tpdi', methods=['POST'])
def recalculate_tpdi(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    TPDIEngine.calculate(teacher)
    db.session.commit()
    return jsonify({'tpdi_score': teacher.tpdi_score, 'tpdi_category': teacher.tpdi_category})
