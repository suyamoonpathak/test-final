from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import path
from .secrets import DATABASE_PATH, JWT_SECRET


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET

db = SQLAlchemy(app)
jwt = JWTManager(app)

from .authentication import authentication
from .questions import questions
from .votes import votes
from .answers import answers

app.register_blueprint(authentication, url_prefix="/")
app.register_blueprint(questions, url_prefix="/")
app.register_blueprint(votes, url_prefix="/")
app.register_blueprint(answers, url_prefix="/")

@app.route('/',methods=['GET'])
def helloWorld():
    return ("Backend Server running!")


from .models import User
with app.app_context():
    db.create_all()