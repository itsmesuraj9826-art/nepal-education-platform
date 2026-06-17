"""
Phase 5 - AI Examination Generation Service
Extracts curriculum content from PDFs, generates question banks,
and assembles exam papers with answer keys.
"""
import json
from flask import current_app
from app.extensions import db
from app.models.exam import Exam, Question
from app.services.ai_service import AIService


class ExamGeneratorService:

    QUESTION_DISTRIBUTION = {
        'easy':   {'mcq': 0.4, 'true_false': 0.1, 'fill_blank': 0.15, 'short_answer': 0.2, 'long_answer': 0.15},
        'medium': {'mcq': 0.3, 'true_false': 0.1, 'fill_blank': 0.1, 'short_answer': 0.25, 'long_answer': 0.25},
        'hard':   {'mcq': 0.2, 'true_false': 0.1, 'fill_blank': 0.1, 'short_answer': 0.25, 'long_answer': 0.25, 'critical_thinking': 0.1},
        'mixed':  {'mcq': 0.3, 'true_false': 0.1, 'fill_blank': 0.1, 'short_answer': 0.2, 'long_answer': 0.2, 'critical_thinking': 0.1},
    }

    @classmethod
    def generate(cls, subject, grade, exam_type, difficulty, total_marks,
                 school_id=None, curriculum_pdf=None):
        curriculum_text = ''
        if curriculum_pdf:
            curriculum_text = cls._extract_pdf(curriculum_pdf)

        exam = Exam(
            title=subject + ' ' + exam_type.title() + ' Examination - Grade ' + str(grade),
            subject=subject,
            grade=grade,
            exam_type=exam_type,
            difficulty=difficulty,
            total_marks=total_marks,
            pass_marks=int(total_marks * 0.4),
            school_id=school_id,
            ai_generated=True,
            status='draft',
            curriculum_src=curriculum_pdf,
        )
        db.session.add(exam)
        db.session.flush()

        questions_data = cls._generate_questions(subject, grade, difficulty, total_marks, curriculum_text)

        for i, q in enumerate(questions_data, 1):
            question = Question(
                exam_id=exam.id,
                question_no=i,
                question_type=q.get('type', 'short_answer'),
                question_text=q.get('question', ''),
                options=json.dumps(q.get('options')) if q.get('options') else None,
                correct_answer=q.get('answer', ''),
                marks=q.get('marks', 1.0),
                difficulty=q.get('difficulty', difficulty),
                chapter=q.get('chapter', ''),
                topic=q.get('topic', ''),
                bloom_level=q.get('bloom_level', 'remember'),
            )
            db.session.add(question)

        db.session.commit()
        return exam

    @classmethod
    def _generate_questions(cls, subject, grade, difficulty, total_marks, curriculum_text):
        dist = cls.QUESTION_DISTRIBUTION.get(difficulty, cls.QUESTION_DISTRIBUTION['mixed'])
        system = (
            "You are an expert Nepal NEB curriculum exam setter. "
            "Generate questions in valid JSON format only."
        )
        curriculum_section = ('Curriculum content:\n' + curriculum_text[:3000]) if curriculum_text else ''
        prompt = (
            "Generate an exam question bank for:\n"
            "- Subject: " + subject + "\n"
            "- Grade: " + str(grade) + "\n"
            "- Total Marks: " + str(total_marks) + "\n"
            "- Difficulty: " + difficulty + "\n"
            "- Distribution: " + json.dumps(dist) + "\n\n"
            + curriculum_section + "\n\n"
            "Return a JSON array. Each item must have: type, question, options (MCQ only), "
            "answer, marks, chapter, topic, bloom_level, difficulty."
        )
        try:
            return AIService.complete_json(prompt, system=system)
        except Exception as e:
            current_app.logger.error('AI question generation failed: ' + str(e))
            return cls._sample_questions(subject, grade, total_marks)

    @staticmethod
    def _extract_pdf(pdf_path):
        try:
            import pdfplumber
            text = ''
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[:20]:
                    text += (page.extract_text() or '') + '\n'
            return text
        except Exception:
            return ''

    @staticmethod
    def _sample_questions(subject, grade, total_marks):
        return [
            {
                'type': 'mcq',
                'question': 'Sample MCQ for ' + subject + ' Grade ' + str(grade),
                'options': ['A) Option A', 'B) Option B', 'C) Option C', 'D) Option D'],
                'answer': 'A) Option A',
                'marks': 1,
                'chapter': 'Chapter 1',
                'topic': 'Introduction',
                'bloom_level': 'remember',
                'difficulty': 'easy',
            },
            {
                'type': 'short_answer',
                'question': 'Explain the main concept of ' + subject + '.',
                'answer': 'Model answer here.',
                'marks': 5,
                'chapter': 'Chapter 1',
                'topic': 'Core Concepts',
                'bloom_level': 'understand',
                'difficulty': 'medium',
            },
            {
                'type': 'long_answer',
                'question': 'Write a detailed essay on a key topic in ' + subject + '.',
                'answer': 'Detailed model answer here.',
                'marks': 10,
                'chapter': 'Chapter 2',
                'topic': 'Advanced Topics',
                'bloom_level': 'evaluate',
                'difficulty': 'hard',
            },
        ]
