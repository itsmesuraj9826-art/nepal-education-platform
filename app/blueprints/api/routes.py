"""
REST API v1 — all endpoints return JSON.
JWT authentication required except /health.
"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.blueprints.api import api_bp
from app.models import School, Teacher, Student
from app.models.attendance import TeacherAttendance, StudentAttendance
from app.models.exam import Exam, StudentResult
from app.extensions import db


@api_bp.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'Nepal Education Platform API v1'})


# ── Schools ───────────────────────────────────────────────
@api_bp.route('/schools')
@jwt_required()
def schools_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    province_id = request.args.get('province_id', type=int)

    query = School.query.filter_by(status='active')
    if province_id:
        query = query.filter_by(province_id=province_id)

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'total': paginated.total,
        'pages': paginated.pages,
        'page': page,
        'data': [s.to_dict() for s in paginated.items],
    })


@api_bp.route('/schools/<int:school_id>')
@jwt_required()
def school_detail(school_id):
    school = School.query.get_or_404(school_id)
    return jsonify(school.to_dict())


# ── Teachers ──────────────────────────────────────────────
@api_bp.route('/teachers')
@jwt_required()
def teachers_list():
    page = request.args.get('page', 1, type=int)
    school_id = request.args.get('school_id', type=int)

    query = Teacher.query.filter_by(is_active=True)
    if school_id:
        query = query.filter_by(school_id=school_id)

    paginated = query.paginate(page=page, per_page=25, error_out=False)
    return jsonify({
        'total': paginated.total,
        'data': [t.to_dict() for t in paginated.items],
    })


@api_bp.route('/teachers/<int:teacher_id>')
@jwt_required()
def teacher_detail(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return jsonify(teacher.to_dict())


# ── Students ──────────────────────────────────────────────
@api_bp.route('/students')
@jwt_required()
def students_list():
    page = request.args.get('page', 1, type=int)
    school_id = request.args.get('school_id', type=int)

    query = Student.query.filter_by(is_active=True)
    if school_id:
        query = query.filter_by(school_id=school_id)

    paginated = query.paginate(page=page, per_page=25, error_out=False)
    return jsonify({
        'total': paginated.total,
        'data': [s.to_dict() for s in paginated.items],
    })


# ── Attendance ────────────────────────────────────────────
@api_bp.route('/attendance/teacher/<int:teacher_id>')
@jwt_required()
def teacher_attendance(teacher_id):
    month = request.args.get('month', type=int)
    year  = request.args.get('year', type=int)
    query = TeacherAttendance.query.filter_by(teacher_id=teacher_id)
    if month and year:
        from sqlalchemy import extract
        query = query.filter(
            extract('month', TeacherAttendance.date) == month,
            extract('year',  TeacherAttendance.date) == year,
        )
    records = query.order_by(TeacherAttendance.date.desc()).all()
    return jsonify([r.to_dict() for r in records])


# ── Analytics ─────────────────────────────────────────────
@api_bp.route('/analytics/national')
@jwt_required()
def national_analytics():
    return jsonify({
        'total_schools':  School.query.filter_by(status='active').count(),
        'total_teachers': Teacher.query.filter_by(is_active=True).count(),
        'total_students': Student.query.filter_by(is_active=True).count(),
        'fraud_alerts':   TeacherAttendance.query.filter_by(fraud_flag=True).count(),
    })
