from flask import Blueprint,request,jsonify
from .models import Answer
from . import db
from datetime import datetime
from zoneinfo import ZoneInfo
from os import path
import os
from werkzeug.utils import secure_filename

answers = Blueprint("answers", __name__)

@answers.route('/api/questions/<int:question_id>/answers', methods=['POST'])
def create_answer(question_id):
    data = request.get_json()
    user_id = data.get('user_id')
    answer_text = data.get('answer')

    if not user_id or not answer_text:
        return jsonify({'message': 'User ID and Answer text are required.'}), 400

    new_answer = Answer(
        answer=answer_text,
        author=user_id,
        question_id=question_id,
        date_created=datetime.now(tz=ZoneInfo('Asia/Kolkata'))
    )

    db.session.add(new_answer)
    db.session.commit()

    return jsonify({'message': 'Answer created successfully.'}), 201

@answers.route('/api/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
def update_answer(question_id, answer_id):
    data = request.get_json()
    user_id = data.get('user_id')
    answer_text = data.get('answer')

    answer = Answer.query.get(answer_id)

    if not answer:
        return jsonify({'message': 'Answer not found.'}), 404

    if answer.author != user_id:
        return jsonify({'message': 'You do not have permission to update this answer.'}), 403

    if not answer_text:
        return jsonify({'message': 'Answer text is required.'}), 400

    answer.answer = answer_text
    db.session.commit()

    return jsonify({'message': 'Answer updated successfully.'}), 200


@answers.route('/api/questions/<int:question_id>/answers/<int:answer_id>', methods=['DELETE'])
def delete_answer(question_id, answer_id):
    data = request.get_json()
    user_id = data.get('user_id')

    answer = Answer.query.get(answer_id)

    if not answer:
        return jsonify({'message': 'Answer not found.'}), 404

    if answer.author != user_id:
        return jsonify({'message': 'You do not have permission to delete this answer.'}), 403

    db.session.delete(answer)
    db.session.commit()

    return jsonify({'message': 'Answer deleted successfully.'}), 200
