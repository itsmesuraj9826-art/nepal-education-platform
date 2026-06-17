from datetime import datetime
from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action      = db.Column(db.String(50), nullable=False)
    # CREATE | UPDATE | DELETE | LOGIN | LOGOUT | SYNC | EXPORT
    entity_type = db.Column(db.String(50))   # School | Teacher | Student | Exam | ...
    entity_id   = db.Column(db.Integer)
    old_value   = db.Column(db.Text)         # JSON snapshot before change
    new_value   = db.Column(db.Text)         # JSON snapshot after change
    ip_address  = db.Column(db.String(45))
    user_agent  = db.Column(db.String(255))
    notes       = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat(),
        }
