from flask import render_template, request, jsonify, redirect, url_for, flash
from app.blueprints.schools import schools_bp
from app.models.school import School
from app.extensions import db
from app.services.school_sync import SchoolSyncService


@schools_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    province_id = request.args.get('province_id', type=int)
    district_id = request.args.get('district_id', type=int)
    status = request.args.get('status', 'active')

    query = School.query
    if search:
        query = query.filter(School.name_en.ilike(f'%{search}%'))
    if province_id:
        query = query.filter_by(province_id=province_id)
    if district_id:
        query = query.filter_by(district_id=district_id)
    if status:
        query = query.filter_by(status=status)

    schools = query.paginate(page=page, per_page=25, error_out=False)
    return render_template('schools/index.html', schools=schools, search=search)


@schools_bp.route('/<int:school_id>')
def detail(school_id):
    school = School.query.get_or_404(school_id)
    return render_template('schools/detail.html', school=school)


@schools_bp.route('/sync', methods=['POST'])
def sync():
    """Trigger manual EMIS sync."""
    result = SchoolSyncService.run_sync()
    flash(f"Sync complete: {result['added']} added, {result['updated']} updated.", 'success')
    return redirect(url_for('schools.index'))


@schools_bp.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    schools = School.query.filter(School.name_en.ilike(f'%{q}%')).limit(20).all()
    return jsonify([s.to_dict() for s in schools])
