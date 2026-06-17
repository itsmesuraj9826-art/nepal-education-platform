from flask import request, jsonify, render_template
from datetime import date, datetime
from app.blueprints.attendance import attendance_bp
from app.models.attendance import TeacherAttendance
from app.models.teacher import Teacher
from app.extensions import db
from app.services.attendance_fraud import FraudDetector


@attendance_bp.route('/')
def index():
    today = date.today()
    records = (TeacherAttendance.query
               .filter_by(date=today)
               .order_by(TeacherAttendance.created_at.desc())
               .limit(100).all())
    return render_template('attendance/index.html', records=records, today=today)


@attendance_bp.route('/checkin', methods=['POST'])
def checkin():
    """GPS + optional photo check-in from mobile app."""
    data = request.get_json()
    teacher_id   = data.get('teacher_id')
    lat          = data.get('latitude')
    lon          = data.get('longitude')
    photo_b64    = data.get('photo')        # base64 image for face verification
    method       = data.get('method', 'mobile_app')

    teacher = Teacher.query.filter_by(teacher_id=teacher_id, is_active=True).first()
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404

    school = teacher.school
    today  = date.today()

    # Geo-fence check
    geo_valid = True
    if lat and lon and school.latitude and school.longitude:
        from geopy.distance import geodesic
        dist_m = geodesic((lat, lon), (school.latitude, school.longitude)).meters
        geo_valid = dist_m <= 200   # within 200 m of school

    # Fraud analysis
    fraud_info = FraudDetector.analyze(teacher, today, lat, lon)

    record = TeacherAttendance.query.filter_by(teacher_id=teacher.id, date=today).first()
    if record:
        return jsonify({'error': 'Already checked in today'}), 409

    record = TeacherAttendance(
        teacher_id=teacher.id,
        school_id=teacher.school_id,
        date=today,
        check_in_time=datetime.utcnow().time(),
        status='present' if geo_valid else 'suspicious',
        method=method,
        check_in_lat=lat,
        check_in_lon=lon,
        geo_valid=geo_valid,
        fraud_flag=fraud_info['flagged'],
        fraud_reason=fraud_info.get('reason'),
        fraud_score=fraud_info.get('score', 0.0),
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'message': 'Check-in recorded', 'geo_valid': geo_valid,
                    'fraud_flag': fraud_info['flagged']})


@attendance_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    lat = data.get('latitude')
    lon = data.get('longitude')

    teacher = Teacher.query.filter_by(teacher_id=teacher_id, is_active=True).first()
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404

    today = date.today()
    record = TeacherAttendance.query.filter_by(teacher_id=teacher.id, date=today).first()
    if not record:
        return jsonify({'error': 'No check-in found for today'}), 404

    record.check_out_time = datetime.utcnow().time()
    record.check_out_lat  = lat
    record.check_out_lon  = lon
    db.session.commit()

    return jsonify({'message': 'Check-out recorded'})


@attendance_bp.route('/fraud-alerts')
def fraud_alerts():
    flagged = (TeacherAttendance.query
               .filter_by(fraud_flag=True)
               .order_by(TeacherAttendance.date.desc())
               .limit(50).all())
    return render_template('attendance/fraud_alerts.html', records=flagged)
