from flask import Blueprint, request, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime
import re

authentication = Blueprint("authentication", __name__)

@authentication.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    terms = data.get('terms')

    if not terms:
        return jsonify({'message': 'Please accept the terms first'}), 400


    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required.'}), 400

    # Check if the email is already taken
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email address already registered. Please use a different email.'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username address already registered. Please use a different username.'}), 400
    
    if not re.search('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'message':"Please choose a valid email."}),400
    
    if not re.search('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{5,}$', password):
        return jsonify({'message':"Password should be at least 5 characters long with at least a special character, an uppercase letter and a digit."}),400

    new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'),last_visit=datetime.now()
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify({'message': 'User signup successful.', 'access_token': access_token}), 201

@authentication.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password.'}), 401

    if user:
        user.last_visit = datetime.now()
        db.session.commit()

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200