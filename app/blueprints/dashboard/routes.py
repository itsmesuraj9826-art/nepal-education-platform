from flask import render_template, session, redirect, url_for
from app.blueprints.dashboard import dashboard_bp
from app.models import School, Teacher, Student
from app.extensions import db
from sqlalchemy import func


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def _national_stats():
    return {
        'total_schools':  School.query.filter_by(status='active').count(),
        'total_teachers': Teacher.query.filter_by(is_active=True).count(),
        'total_students': Student.query.filter_by(is_active=True).count(),
    }


@dashboard_bp.route('/principal')
@login_required
def principal():
    school_id = session.get('school_id')
    stats = {
        'teachers': Teacher.query.filter_by(school_id=school_id, is_active=True).count(),
        'students': Student.query.filter_by(school_id=school_id, is_active=True).count(),
    }
    school = School.query.get(school_id)
    return render_template('dashboard/principal.html', stats=stats, school=school)


@dashboard_bp.route('/municipality')
@login_required
def municipality():
    mun_id = session.get('municipality_id')
    schools = School.query.filter_by(municipality_id=mun_id, status='active').all()
    stats = {
        'total_schools': len(schools),
        'total_teachers': sum(s.num_teachers for s in schools),
        'total_students': sum(s.num_students for s in schools),
    }
    return render_template('dashboard/municipality.html', stats=stats, schools=schools)


@dashboard_bp.route('/district')
@login_required
def district():
    district_id = session.get('district_id')
    from app.models.school import Municipality
    muns = Municipality.query.filter_by(district_id=district_id).all()
    schools = School.query.filter_by(district_id=district_id, status='active').all()
    stats = {
        'total_schools': len(schools),
        'total_municipalities': len(muns),
        'total_teachers': sum(s.num_teachers for s in schools),
        'total_students': sum(s.num_students for s in schools),
    }
    return render_template('dashboard/district.html', stats=stats, municipalities=muns)


@dashboard_bp.route('/provincial', methods=['GET', 'POST'])
@login_required
def provincial():
    province_id = session.get('province_id')
    from app.models.school import District, Province
    province  = Province.query.get(province_id)
    districts = District.query.filter_by(province_id=province_id).all()
    schools   = School.query.filter_by(province_id=province_id, status='active').all()

    if request.method == 'POST' and session.get('role') == 'provincial':
        edd_head = request.form.get('edd_head', '').strip()
        if province and edd_head:
            province.edd_head = edd_head
            db.session.commit()
            flash('EDD head updated.', 'success')
        return redirect(url_for('dashboard.provincial'))

    stats = {
        'total_schools':   len(schools),
        'total_districts': len(districts),
        'total_teachers':  sum(s.num_teachers or 0 for s in schools),
        'total_students':  sum(s.num_students or 0 for s in schools),
    }
    return render_template('dashboard/provincial.html',
                           stats=stats, districts=districts, province=province)


@dashboard_bp.route('/school')
@login_required
def school():
    school_id = session.get('school_id')
    school = School.query.get(school_id)
    teachers = Teacher.query.filter_by(school_id=school_id, is_active=True).all()
    students = Student.query.filter_by(school_id=school_id, is_active=True).all()
    stats = {
        'total_teachers': len(teachers),
        'total_students': len(students),
        'total_male':   sum(1 for s in students if s.gender == 'male'),
        'total_female': sum(1 for s in students if s.gender == 'female'),
    }
    return render_template('dashboard/school.html', school=school, stats=stats,
                           teachers=teachers, students=students)


@dashboard_bp.route('/federal')
@login_required
def federal():
    stats = _national_stats()
    from app.models.school import Province
    provinces = Province.query.all()
    # Enrich provinces with their school/student/teacher counts
    province_stats = []
    for p in provinces:
        p_schools = School.query.filter_by(province_id=p.id, status='active').all()
        province_stats.append({
            'province':       p,
            'total_schools':  len(p_schools),
            'total_students': sum(s.num_students or 0 for s in p_schools),
            'total_teachers': sum(s.num_teachers or 0 for s in p_schools),
            'edd_head':       p.edd_head or '—',
        })
    minister = {
        'name':  'Mahabir Pun',
        'title': 'Minister for Education, Science and Technology',
        'since': 'September 2025',
        'govt':  'Government of Nepal',
    }
    return render_template('dashboard/federal.html',
                           stats=stats, province_stats=province_stats, minister=minister)
