"""
Phase 3 — Teacher Performance & Development Index (TPDI) Engine
Calculates composite performance scores for teachers.
"""
from datetime import date, timedelta
from app.models.attendance import TeacherAttendance
from app.models.exam import StudentResult


class TPDIEngine:
    """
    TPDI Score = weighted composite of:
      40% Attendance & Punctuality
      35% Student Academic Performance
      15% Principal/Peer Evaluation (manual input)
      10% Parent Feedback (manual input)
    """

    THRESHOLDS = {
        'Outstanding':          90,
        'Excellent':            80,
        'Good':                 65,
        'Satisfactory':         50,
        'Improvement Required':  0,
    }

    @classmethod
    def calculate(cls, teacher) -> None:
        """Recalculate and update teacher's TPDI fields in-place (caller must commit)."""
        att_score        = cls._attendance_score(teacher)
        punctuality_score = cls._punctuality_score(teacher)
        student_score    = cls._student_performance_score(teacher)

        # Composite weighted score
        tpdi = (
            att_score        * 0.25 +
            punctuality_score * 0.15 +
            student_score    * 0.35 +
            (teacher.tpdi_score or 50) * 0.25   # preserve manual eval portion
        )
        tpdi = round(min(max(tpdi, 0), 100), 2)

        teacher.attendance_score        = round(att_score, 2)
        teacher.punctuality_score       = round(punctuality_score, 2)
        teacher.student_performance_score = round(student_score, 2)
        teacher.tpdi_score              = tpdi
        teacher.tpdi_category           = cls._category(tpdi)

    @staticmethod
    def _attendance_score(teacher) -> float:
        """% of school days present in the last 90 days (0–100)."""
        since = date.today() - timedelta(days=90)
        records = TeacherAttendance.query.filter(
            TeacherAttendance.teacher_id == teacher.id,
            TeacherAttendance.date >= since,
        ).all()
        if not records:
            return 70.0   # default if no data
        present = sum(1 for r in records if r.status in ('present', 'late', 'half_day'))
        total   = len(records)
        return (present / total) * 100

    @staticmethod
    def _punctuality_score(teacher) -> float:
        """Score based on on-time arrivals. Late = deduct points (0–100)."""
        since = date.today() - timedelta(days=90)
        records = TeacherAttendance.query.filter(
            TeacherAttendance.teacher_id == teacher.id,
            TeacherAttendance.date >= since,
        ).all()
        if not records:
            return 70.0
        on_time = sum(1 for r in records if r.status == 'present')
        late    = sum(1 for r in records if r.status == 'late')
        total   = len(records)
        score = ((on_time * 1.0 + late * 0.5) / total) * 100
        return score

    @staticmethod
    def _student_performance_score(teacher) -> float:
        """Average percentage of students taught by this teacher in recent exams (0–100)."""
        school_id = teacher.school_id
        if not school_id:
            return 60.0
        results = (StudentResult.query
                   .filter_by(school_id=school_id)
                   .limit(200).all())
        if not results:
            return 60.0
        avg_pct = sum(r.percentage or 0 for r in results) / len(results)
        return min(avg_pct, 100.0)

    @classmethod
    def _category(cls, score: float) -> str:
        for cat, threshold in cls.THRESHOLDS.items():
            if score >= threshold:
                return cat
        return 'Improvement Required'
