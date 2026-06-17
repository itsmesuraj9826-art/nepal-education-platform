import os
from app import create_app
from app.extensions import db

app = create_app(os.getenv('FLASK_ENV', 'production'))


def _init_db():
    """Create tables and seed admin user on first run."""
    with app.app_context():
        db.create_all()

        # Seed provinces if empty
        from app.models.school import Province
        if Province.query.count() == 0:
            provinces = [
                Province(id=1, name='Koshi Province',         name_np='कोशी प्रदेश',          code='P1'),
                Province(id=2, name='Madhesh Province',       name_np='मधेश प्रदेश',          code='P2'),
                Province(id=3, name='Bagmati Province',       name_np='बागमती प्रदेश',        code='P3'),
                Province(id=4, name='Gandaki Province',       name_np='गण्डकी प्रदेश',        code='P4'),
                Province(id=5, name='Lumbini Province',       name_np='लुम्बिनी प्रदेश',      code='P5'),
                Province(id=6, name='Karnali Province',       name_np='कर्णाली प्रदेश',       code='P6'),
                Province(id=7, name='Sudurpashchim Province', name_np='सुदूरपश्चिम प्रदेश',   code='P7'),
            ]
            db.session.add_all(provinces)
            db.session.commit()

        # Seed admin user if missing
        from app.models.user import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@nepal-edu.gov.np',
                full_name='System Administrator',
                role='federal',
                is_active=True,
            )
            admin.set_password('Admin@Nepal2026')
            db.session.add(admin)
            db.session.commit()


_init_db()
