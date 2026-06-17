"""
Phase 2 — Attendance Fraud Detection Service
Identifies proxy attendance, suspicious GPS patterns,
repeated late arrivals, and other anomalies.
"""
from datetime import date, timedelta
from app.models.attendance import TeacherAttendance


class FraudDetector:

    @staticmethod
    def analyze(teacher, check_date: date, lat: float = None, lon: float = None) -> dict:
        """
        Run all fraud checks for a check-in attempt.
        Returns dict with 'flagged' bool, 'reason', and 'score' (0–1).
        """
        flags = []
        score = 0.0

        # Check 1: Rapid duplicate (already checked in from different location)
        existing = TeacherAttendance.query.filter_by(
            teacher_id=teacher.id, date=check_date).first()
        if existing:
            flags.append('duplicate_checkin')
            score += 0.9

        # Check 2: GPS outside school boundary (handled in route, but log here)
        school = teacher.school
        if lat and lon and school and school.latitude and school.longitude:
            from geopy.distance import geodesic
            dist = geodesic((lat, lon), (school.latitude, school.longitude)).meters
            if dist > 500:
                flags.append(f'gps_too_far_{int(dist)}m')
                score += 0.6
            elif dist > 200:
                flags.append(f'gps_borderline_{int(dist)}m')
                score += 0.2

        # Check 3: Unusual time (before 5 AM or after 10 PM)
        from datetime import datetime
        now_hour = datetime.utcnow().hour + 5  # Nepal is UTC+5:45; approximate
        if now_hour < 5 or now_hour > 22:
            flags.append('unusual_checkin_time')
            score += 0.3

        # Check 4: Pattern — more than 3 consecutive lates in last 10 days
        recent = (TeacherAttendance.query
                  .filter_by(teacher_id=teacher.id)
                  .filter(TeacherAttendance.date >= check_date - timedelta(days=10))
                  .order_by(TeacherAttendance.date.desc())
                  .all())
        late_streak = sum(1 for r in recent if r.status in ('late', 'suspicious'))
        if late_streak >= 3:
            flags.append(f'repeated_late_{late_streak}x_in_10_days')
            score += 0.25

        # Check 5: Check if teacher was absent yesterday but present today
        yesterday = check_date - timedelta(days=1)
        yesterday_rec = TeacherAttendance.query.filter_by(
            teacher_id=teacher.id, date=yesterday).first()
        if yesterday_rec and yesterday_rec.status == 'absent':
            score += 0.05   # minor flag

        score = min(score, 1.0)
        flagged = score >= 0.5 or 'duplicate_checkin' in flags

        return {
            'flagged': flagged,
            'reason': '; '.join(flags) if flags else None,
            'score': round(score, 3),
        }
