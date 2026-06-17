from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, unset_jwt_cookies
)
from app.blueprints.auth import auth_bp
from app.models.user import User
from app.extensions import db
from datetime import datetime


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') or request.json.get('username')
        password = request.form.get('password') or request.json.get('password')

        user = User.query.filter_by(username=username, is_active=True).first()
        if not user or not user.check_password(password):
            if request.is_json:
                return jsonify({'error': 'Invalid credentials'}), 401
            flash('Invalid username or password.', 'danger')
            return render_template('auth/login.html')

        user.last_login = datetime.utcnow()
        db.session.commit()

        access_token  = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        if request.is_json:
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token,
                            'user': user.to_dict()})

        # Web login — set cookie and redirect by role
        from flask import session
        session['user_id'] = user.id
        session['role']    = user.role
        return redirect(url_for(f'dashboard.{user.role}'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    from flask import session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token})
