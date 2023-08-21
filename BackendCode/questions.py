from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint,request,jsonify
from .models import Question
from . import db
from datetime import datetime
from zoneinfo import ZoneInfo
from os import path
import os
from werkzeug.utils import secure_filename

questions = Blueprint("questions", __name__)

UPLOAD_FOLDER = path.join(path.dirname(
    path.realpath(__file__)), 'static/QuestionImages')

@questions.route('/api/<int:user_id>/questions', methods=['POST'])
def create_question(user_id):
    data = request.form  # Use form data to handle both text and file fields
    title = data.get('title')
    description = data.get('description')
    uploaded_file = request.files.get('image')  # Get the uploaded file

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