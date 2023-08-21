from flask import Blueprint,request,jsonify
from .models import Question, Answer, QuestionVote, AnswerVote
from . import db
from datetime import datetime
from zoneinfo import ZoneInfo
from os import path
import os
from werkzeug.utils import secure_filename

questions = Blueprint("questions", __name__)

UPLOAD_FOLDER = path.join(path.dirname(
    path.realpath(__file__)), 'static/QuestionImages')

@questions.route('/api/questions', methods=['GET'])
def get_all_questions():
    questions = Question.query.all()

    question_list = []
    for question in questions:
        question_data = {
            'id': question.id,
            'title': question.title,
            'description': question.description,
            'author': question.author,
            'date_created': question.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'fileName': question.fileName,
            'answers': [],
            'votes': [],
        }

        question_votes = QuestionVote.query.filter_by(question_id=question.id).all()
        question_data['votes'] = [vote.value for vote in question_votes]

        answers = Answer.query.filter_by(question_id=question.id).all()
        for answer in answers:
            answer_data = {
                'id': answer.id,
                'answer': answer.answer,
                'date_created': answer.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'author': answer.author,
                'votes': [],
            }

            answer_votes = AnswerVote.query.filter_by(answer_id=answer.id).all()
            answer_data['votes'] = [vote.value for vote in answer_votes]

            question_data['answers'].append(answer_data)

        question_list.append(question_data)

    return jsonify({'questions': question_list})

@questions.route('/api/<int:user_id>/questions', methods=['POST'])
def create_question(user_id):
    data = request.form
    title = data.get('title')
    description = data.get('description')
    uploaded_file = request.files.get('image')
    if not title or not description:
        return jsonify({'message': 'Title and description are required.'}), 400

    new_question = Question(
        title=title,
        description=description,
        author=user_id,
        date_created=datetime.now(tz=ZoneInfo('Asia/Kolkata'))
    )

    db.session.add(new_question)
    db.session.commit()

    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))

        new_question.fileName = filename
        db.session.commit()

    return jsonify({'message': 'Question created successfully.'}), 201

@questions.route('/api/<int:user_id>/questions/<int:question_id>', methods=['PUT'])
def update_question(user_id, question_id):
    data = request.form
    title = data.get('title')
    description = data.get('description')
    uploaded_file = request.files.get('image')

    question = Question.query.get(question_id)

    if not question:
        return jsonify({'message': 'Question not found.'}), 404

    if question.author != user_id:
        return jsonify({'message': 'You do not have permission to update this question.'}), 403

    if not title or not description:
        return jsonify({'message': 'Title and description are required.'}), 400

    question.title = title
    question.description = description
    db.session.commit()

    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))

        question.fileName = filename
        db.session.commit()

    return jsonify({'message': 'Question updated successfully.'}), 200

@questions.route('/api/<int:user_id>/questions/<int:question_id>', methods=['DELETE'])
def delete_question(user_id, question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({'message': 'Question not found.'}), 404

    if question.author != user_id:
        return jsonify({'message': 'You do not have permission to delete this question.'}), 403

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': 'Question deleted successfully.'}), 200

