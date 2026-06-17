"""
Phase 6 — AI OCR Answer Sheet Evaluation
Processes scanned answer sheet images, extracts handwritten text,
compares with answer keys, and auto-generates marks.
"""
import json
import os
from flask import current_app
from app.extensions import db
from app.models.exam import StudentResult, AnswerSheet, Question
from app.services.ai_service import AIService


class OCRService:

    @classmethod
    def evaluate_answer_sheet(cls, image_paths: list, exam, result: StudentResult) -> dict:
        """
        1. OCR each page image.
        2. Combine OCR text.
        3. AI evaluates against answer key.
        4. Save AnswerSheet record, update StudentResult.
        Returns evaluation dict.
        """
        # Step 1: OCR all pages
        ocr_texts = [cls._ocr_image(p) for p in image_paths]
        combined_text = '\n--- PAGE BREAK ---\n'.join(ocr_texts)

        # Step 2: Load answer key
        questions = Question.query.filter_by(exam_id=exam.id).order_by(Question.question_no).all()
        answer_key = [
            {'q_no': q.question_no, 'question': q.question_text,
             'answer': q.correct_answer, 'marks': q.marks, 'type': q.question_type}
            for q in questions
        ]

        # Step 3: AI evaluation
        evaluation = cls._ai_evaluate(combined_text, answer_key, exam)

        # Step 4: Persist
        sheet = AnswerSheet(
            result_id=result.id,
            image_urls=json.dumps(image_paths),
            ocr_text=combined_text,
            ai_marks_json=json.dumps(evaluation.get('question_marks', [])),
            ocr_confidence=evaluation.get('ocr_confidence', 0.0),
            processed_at=__import__('datetime').datetime.utcnow(),
        )
        db.session.add(sheet)

        result.marks_obtained = evaluation.get('total_marks_obtained', 0)
        result.percentage     = round(
            (result.marks_obtained / exam.total_marks) * 100, 2
        ) if exam.total_marks else 0
        result.grade          = cls._grade(result.percentage)
        result.ai_evaluated   = True
        result.subject_breakdown = json.dumps(evaluation.get('question_marks', []))

        db.session.commit()
        return evaluation

    @staticmethod
    def _ocr_image(image_path: str) -> str:
        """Extract text from image using Tesseract + OpenCV preprocessing."""
        try:
            import cv2
            import pytesseract
            import numpy as np

            pytesseract.pytesseract.tesseract_cmd = current_app.config.get(
                'TESSERACT_CMD', '/usr/bin/tesseract')

            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Denoise + threshold for handwriting
            denoised = cv2.fastNlMeansDenoising(gray, h=10)
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            text = pytesseract.image_to_string(
                thresh,
                lang='eng+nep',   # English + Nepali
                config='--psm 6',
            )
            return text.strip()
        except Exception as e:
            current_app.logger.error(f'OCR failed for {image_path}: {e}')
            return ''

    @staticmethod
    def _ai_evaluate(ocr_text: str, answer_key: list, exam) -> dict:
        """Use AI to compare student answers with the answer key."""
        system = (
            "You are a strict but fair Nepal NEB examiner. "
            "Evaluate student answers against the official answer key and assign marks. "
            "Return JSON only."
        )
        prompt = f"""
Exam: {exam.title}  Subject: {exam.subject}  Total Marks: {exam.total_marks}

ANSWER KEY:
{json.dumps(answer_key, indent=2)}

STUDENT'S OCR-EXTRACTED ANSWERS:
{ocr_text[:4000]}

Evaluate each question and return JSON:
{{
  "question_marks": [
    {{"q_no": 1, "marks_awarded": 2, "max_marks": 2, "feedback": "correct"}},
    ...
  ],
  "total_marks_obtained": 45,
  "ocr_confidence": 0.85,
  "overall_feedback": "Good performance in chapters 1-3, weak in chapter 4."
}}
"""
        try:
            return AIService.complete_json(prompt, system=system)
        except Exception as e:
            current_app.logger.error(f'AI evaluation failed: {e}')
            return {'question_marks': [], 'total_marks_obtained': 0,
                    'ocr_confidence': 0.0, 'overall_feedback': 'AI evaluation failed.'}

    @staticmethod
    def _grade(percentage: float) -> str:
        if percentage >= 90: return 'A+'
        if percentage >= 80: return 'A'
        if percentage >= 70: return 'B+'
        if percentage >= 60: return 'B'
        if percentage >= 50: return 'C+'
        if percentage >= 40: return 'C'
        if percentage >= 35: return 'D'
        return 'E'
