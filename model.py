import select
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Users(db.Model):
    username = db.Column(db.String(15), nullable = False, unique=True)
    name=db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(10),nullable=False)
    user_id = db.Column(db.Integer(), primary_key=True)
    education = db.Column(db.String(100),nullable=False)
    work = db.Column(db.String(100),nullable=False)
    about = db.Column(db.String(1000))
    image=db.Column(db.String(20))
    user_type=db.Column(db.String(25),nullable=False)
    post=db.relationship('Posts',backref='student',cascade='all,delete')
    aptitude_test=db.relationship('Aptitude_test',backref='users',cascade='all,delete')
    test_score=db.relationship('Test_score',backref='users',cascade='all,delete')

class Posts(db.Model):
    post_id=db.Column(db.Integer(), primary_key=True)
    created_by=db.Column(db.Integer(), db.ForeignKey("users.user_id"), nullable=False)
    experiences=db.Column(db.String(1000))
    tips=db.Column(db.String(5000))
    created_at=db.Column(db.String(19), nullable=False)
    likes=db.Column(db.Integer())
    dislikes=db.Column(db.Integer())
    post_comment=db.relationship('Post_comment',backref='posts',cascade='all,delete')

class Post_comment(db.Model):
    post_id=db.Column(db.Integer(),db.ForeignKey("posts.post_id"), primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("users.user_id"), primary_key=True)
    content = db.Column(db.String(5000))

class Aptitude_test(db.Model):
    apti_id=db.Column(db.Integer(), primary_key=True)
    apti_name=db.Column(db.String(200),nullable=False)
    created_by=db.Column(db.Integer(), db.ForeignKey("users.user_id"), nullable=False)
    created_at=db.Column(db.String(19), nullable=False)
    likes=db.Column(db.Integer())
    dislikes=db.Column(db.Integer())
    apti_comment=db.relationship('Apti_comment',backref='aptitude_test',cascade='all,delete')
    test_quest=db.relationship('Test_quest',backref='aptitude_test',cascade='all,delete')
    test_score=db.relationship('Test_score',backref='aptitude_test',cascade='all,delete')

class Apti_comment(db.Model):
    apti_id = db.Column(db.Integer(), db.ForeignKey('aptitude_test.apti_id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), primary_key=True)
    content = db.Column(db.String(5000))

class Test_quest(db.Model):
    apti_id=db.Column(db.Integer(),db.ForeignKey("aptitude_test.apti_id"))
    quest_id=db.Column(db.Integer(), primary_key=True)
    question=db.Column(db.String(1000),nullable=False)
    marks=db.Column(db.Integer(),nullable=False)
    answers=db.Column(db.String(10000),nullable=False)

class Test_score(db.Model):
    apti_id=db.Column(db.Integer(),db.ForeignKey("aptitude_test.apti_id"),primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("users.user_id"),primary_key=True)
    score=db.Column(db.Integer())

class Connection(db.Model):
    user=db.Column(db.Integer(),db.ForeignKey("users.user_id"),primary_key=True)
    following=db.Column(db.Integer(),db.ForeignKey("users.user_id"),primary_key=True)
