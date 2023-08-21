from . import db

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    last_visit = db.Column(db.DateTime)
    questions = db.relationship('Question', backref='user', passive_deletes=True)
    comments = db.relationship('Answer', backref='user', passive_deletes=True)
    votes = db.relationship('QuestionVote', backref='user', passive_deletes=True)
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(
        followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_questions(self):
        followed = Question.query.join(followers, (followers.c.followed_id == Question.author)).filter(
            followers.c.follower_id == self.id).order_by(Question.date_created.desc())
        return followed


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    fileName = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Answer', backref='question', passive_deletes=True)
    votes = db.relationship('QuestionVote', backref='question', passive_deletes=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id', ondelete="CASCADE"), nullable=False)
    answer_votes = db.relationship('AnswerVote', backref='answer', passive_deletes=True)



class QuestionVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=False)
    value = db.Column(db.Integer, nullable=False)


class AnswerVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete="CASCADE"), nullable=False)
    value = db.Column(db.Integer, nullable=False)