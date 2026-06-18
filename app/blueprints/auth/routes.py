from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.blueprints.auth import auth_bp
from app.models.user import User
from app.models.school import School
from app.extensions import db
from datetime import datetime


ROLE_DASHBOARD = {
    'federal':      'dashboard.federal',
    'provincial':   'dashboard.provincial',
    'district':     'dashboard.district',
    'municipality': 'dashboard.municipality',
    'principal':    'dashboard.school',
    'school':       'dashboard.school',
    'teacher':      'dashboard.school',
}


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            _json = request.get_json(silent=True) or {}
            identifier = (request.form.get('username') or _json.get('username', '')).strip()
            password   = request.form.get('password') or _json.get('password', '')

            # 1. Try username or email login
            user = User.query.filter(
                (User.username == identifier) | (User.email == identifier),
                User.is_active == True
            ).first()

            # 2. Try school code login
            if not user:
                school = School.query.filter_by(school_code=identifier).first()
                if school:
                    user = User.query.filter_by(school_id=school.id, role='school').first()
                    if not user:
                        # Auto-create school account — default password is the school code
                        from werkzeug.security import generate_password_hash
                        user = User(
                            username        = school.school_code,
                            email           = f"{school.school_code}@school.edu.np",
                            password_hash   = generate_password_hash(school.school_code),
                            full_name       = school.name_en,
                            role            = 'school',
                            school_id       = school.id,
                            province_id     = school.province_id,
                            district_id     = school.district_id,
                            municipality_id = school.municipality_id,
                            is_active       = True,
                        )
                        db.session.add(user)
                        db.session.commit()

            if not user or not user.check_password(password):
                if request.is_json:
                    return jsonify({'error': 'Invalid credentials'}), 401
                flash('Invalid username, school code, or password.', 'danger')
                return render_template('auth/login.html')

            user.last_login = datetime.utcnow()
            db.session.commit()

            if request.is_json:
                access_token  = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                return jsonify({'access_token': access_token,
                                'refresh_token': refresh_token,
                                'user': user.to_dict()})

            session['user_id']         = user.id
            session['role']            = user.role
            session['full_name']       = user.full_name or user.username
            session['school_id']       = user.school_id
            session['province_id']     = user.province_id
            session['district_id']     = user.district_id
            session['municipality_id'] = user.municipality_id

            return redirect(url_for(ROLE_DASHBOARD.get(user.role, 'dashboard.federal')))

        except Exception as e:
            import traceback
            return jsonify({
                'error_type': type(e).__name__,
                'login_error': str(e),
                'traceback': traceback.format_exc(),
            }), 500

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return jsonify({'access_token': create_access_token(identity=get_jwt_identity())})
