from flask import Blueprint,request,jsonify
from .models import Question, User, QuestionVote, Answer, AnswerVote
from . import db
from datetime import datetime

votes = Blueprint("votes", __name__)

@votes.route('/api/questions/<int:question_id>/vote', methods=['POST'])
def vote_question(question_id):
    data = request.get_json()
    user_id = data.get('user_id')
    value = data.get('value')  # 0 for no vote, 1 for upvote, -1 for downvote

    question = Question.query.get(question_id)
    user = User.query.get(user_id)

    if not question or not user:
        return jsonify({'message': 'Question or user not found.'}), 404

    existing_vote = QuestionVote.query.filter_by(
        author_id=user_id, question_id=question_id).first()

    if existing_vote:
        if existing_vote.value != value:
            existing_vote.value = value
            db.session.commit()
            return jsonify({'message': 'Vote updated successfully.'}), 200
        else:
            return jsonify({'message': 'You have already voted with the same value.'}), 400

    new_vote = QuestionVote(
        author_id=user_id,
        question_id=question_id,
        value=value,
        date_created=datetime.now()
    )

    db.session.add(new_vote)
    question.votes.append(new_vote)
    db.session.commit()

    return jsonify({'message': 'Vote recorded successfully.'}), 201

@votes.route('/api/answers/<int:answer_id>/vote', methods=['POST'])
def vote_answer(answer_id):
    data = request.get_json()
    user_id = data.get('user_id')
    value = data.get('value')  # 0 for no vote, 1 for upvote, -1 for downvote

    answer = Answer.query.get(answer_id)
    user = User.query.get(user_id)

    if not answer or not user:
        return jsonify({'message': 'Answer or user not found.'}), 404

    existing_vote = AnswerVote.query.filter_by(
        author_id=user_id, answer_id=answer_id).first()

    if existing_vote:
        if existing_vote.value != value:
            existing_vote.value = value
            db.session.commit()
            return jsonify({'message': 'Vote updated successfully.'}), 200
        else:
            return jsonify({'message': 'You have already voted with the same value.'}), 400

    new_vote = AnswerVote(
        author_id=user_id,
        answer_id=answer_id,
        value=value,
        date_created=datetime.now()
    )

    db.session.add(new_vote)
    answer.answer_votes.append(new_vote)
    db.session.commit()

    return jsonify({'message': 'Vote recorded successfully.'}), 201

