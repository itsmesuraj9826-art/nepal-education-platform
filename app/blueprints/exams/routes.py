import os
from flask import render_template, request, jsonify, current_app, redirect, url_for, flash
from app.blueprints.exams import exams_bp
from app.models.exam import Exam, Question, StudentResult, AnswerSheet
from app.extensions import db
from app.services.exam_generator import ExamGeneratorService
from app.services.ocr_service import OCRService


@exams_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    exams = Exam.query.order_by(Exam.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('exams/index.html', exams=exams)


@exams_bp.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        subject  = request.form['subject']
        grade    = request.form['grade']
        exam_type = request.form['exam_type']
        difficulty = request.form['difficulty']
        total_marks = int(request.form.get('total_marks', 100))
        school_id = request.form.get('school_id', type=int)

        # Handle uploaded curriculum PDF
        pdf_file = request.files.get('curriculum_pdf')
        pdf_path = None
        if pdf_file:
            upload_dir = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_dir, exist_ok=True)
            pdf_path = os.path.join(upload_dir, pdf_file.filename)
            pdf_file.save(pdf_path)

        exam = ExamGeneratorService.generate(
            subject=subject,
            grade=grade,
            exam_type=exam_type,
            difficulty=difficulty,
            total_marks=total_marks,
            school_id=school_id,
            curriculum_pdf=pdf_path,
        )
        flash(f'Exam "{exam.title}" generated with {exam.questions.count()} questions.', 'success')
        return redirect(url_for('exams.detail', exam_id=exam.id))

    return render_template('exams/generate.html')


@exams_bp.route('/<int:exam_id>')
def detail(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = exam.questions.order_by(Question.question_no).all()
    return render_template('exams/detail.html', exam=exam, questions=questions)


@exams_bp.route('/evaluate-answersheet', methods=['POST'])
def evaluate_answersheet():
    """Upload scanned answer sheet images → AI evaluates → returns marks."""
    result_id = request.form.get('result_id', type=int)
    images    = request.files.getlist('images')
    if not images:
        return jsonify({'error': 'No images uploaded'}), 400

    result = StudentResult.query.get_or_404(result_id)
    exam   = result.exam

    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'answer_sheets')
    os.makedirs(upload_dir, exist_ok=True)
    image_paths = []
    for img in images:
        path = os.path.join(upload_dir, f'{result_id}_{img.filename}')
        img.save(path)
        image_paths.append(path)

    evaluation = OCRService.evaluate_answer_sheet(
        image_paths=image_paths,
        exam=exam,
        result=result,
    )

    return jsonify(evaluation)
