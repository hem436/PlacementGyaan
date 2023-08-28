from flask_restful import Resource, Api, reqparse, fields, abort
import requests
from flask_cors import CORS
from flask import Flask, redirect, render_template, request, send_file, jsonify, json
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
import pandas as pd
import os
from model import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///SE_project.sqlite3'
app.app_context().push()
db.init_app(app)
if not os.path.exists('./instance/SE_project.sqlite3'):
    print("creating database")
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
app.app_context().push()
api = Api(app)
CORS(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def save_image(picture):
    pic_name = secure_filename(picture.filename)
    pic_path = os.path.join('./static/', pic_name)
    picture.save(pic_path)
    return pic_name


def check_username(name):
    user = Users.query.filter_by(name=name).all()
    if user:
        return False
    return True

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

# Sample correct answer and student answer
correct_answer = "The capital of France is Paris."
student_answer = "Germany is not the capital of Mexico."

# Preprocess the text data
def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stopwords.words('english')]
    return ' '.join(words)

def evaluateQ(correct_answer, student_answer):
    # Preprocess the text data
    preprocessed_correct = preprocess_text(correct_answer)
    preprocessed_student = preprocess_text(student_answer)

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocessed_correct, preprocessed_student])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    # Print the cosine similarity
    print("Cosine Similarity:", cosine_sim)
    
    if cosine_sim > 0.5:
        return True
    else:
        return False
print(evaluateQ(correct_answer, student_answer))



@app.route('/')
def index():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('index.html')
        else:
            return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(name=username, password=password).first()
        if user:
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid username or password")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if check_username(username) == False:
            return render_template('signup.html')
        new_user = Users(name=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/posts')
def posts():
    return render_template('posts.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        return render_template('create_post.html')
    elif request.method == 'POST':
        requests.post()


@app.route('/edit_post')
def edit_post():
    if request.method == 'GET':
        return render_template('edit_post.html')
    elif request.method == 'POST':
        requests.put()


@app.route('/assessments')
def assessment():
    if request.method == 'GET':
        return render_template('assessments.html')
    else:
        return


@app.route('/create_assessment')
def assess():
    if request.method == 'GET':
        return render_template('create_assessment.html')

@app.route('/assessment/<int:apti_id>')
def view_assessment(apti_id):
    if request.method == 'GET':
        return render_template('view_assess.html', apti_id=apti_id)
    
@app.route('/connect')
def connect():
    return render_template('connect.html')

class Login_api(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            username = json_data['username']
            password = json_data['password']
            user = Users.query.filter_by(
                name=username, password=password).first()
            if user:
                user_output_fields = {
                    'user_id': user.user_id,
                }
                return jsonify(user_output_fields)
            abort(404, message='Enter the credential correctly')
        except:
            return "server error", 500


api.add_resource(Login_api, '/login')


class Users_api(Resource):
    def get(self):
        try:
            user_id = int(request.args.get('user_id'))
            if user_id != 0:
                user = Users.query.get(user_id)
                if user:
                    user_output_fields = {
                        'user_id': user.user_id,
                        'name': user.name,
                        'img': user.img,
                        'education': user.education,
                        'work': user.work,
                        'about': user.about,
                        'user_type': user.user_type
                    }
                    return jsonify(user_output_fields)
                else:
                    return "no user exit", 405
            elif user_id == 0:
                users = Users.query.all()
                if users:
                    users_output_fields = []
                    for user in users:
                        user_output_fields = {
                            'user_id': user.user_id,
                            'name': user.name,
                            'img': user.img,
                            'education': user.education,
                            'work': user.work,
                            'about': user.about,
                            'user_type': user.user_type
                        }
                        users_output_fields.append(user_output_fields)
                    return jsonify(users_output_fields)
                else:
                    return "no user exit", 405
            else:
                return "invalid user id", 404
        except:
            return "server error", 500

    def post(self):
        try:
            contain_image = bool(int(request.form['contain_image']))
            username = request.form['username']
            name = request.form['name']
            password = request.form['password']
            education = request.form['education']
            work = request.form['work']
            about = request.form['about']
            user_type = "admin" if request.form['user_type'] else "user"
            img = ''
            if contain_image:
                img = save_image(request.files['image'])
            if check_username(username) == False:
                return ('Username aleready exists', 400)
            new_user = Users(username=username, name=name, password=password, img=img,
                             education=education, work=work, about=about, user_type=user_type)
            db.session.add(new_user)
            db.session.commit()
            return "user created", 201
        except:
            return "server error", 500

    def put(self):
        try:
            user_id = request.form['user_id']
            img = save_image(request.files['image'])
            user = Users.query.get(user_id)
            user.img = img
            db.session.commit()
            return 'Picture changed', 201
        except:
            return "server error", 500


api.add_resource(Users_api, "/api/users")


class Posts_api(Resource):
    def get(self, post_id, user_id):
        try:
            user = Users.query.filter_by(user_id=user_id)
            if post_id != 0:  # incase we want to fetch a particular post by user
                post = Posts.query.filter_by(
                    user_id=user_id, id=post_id).first()
                p = {
                    'post_id': post.id,
                    'experiences': post.experiences,
                    'likes': post.likes,
                    'dislikes': post.dislikes,
                    'img': post.images,
                    'tips': post.tips,
                    'created_at': post.created_at,
                    'created_by': user.name
                }
                return jsonify(p)
            else:  # incase we want all the post from any particular user
                posts = Posts.query.filter_by(user_id=user_id).all()
                # print(posts)
                if posts:
                    post_contents = []
                    for post in posts:
                        p = {
                            'post_id': post.id,
                            'experiences': post.experiences,
                            'likes': post.likes,
                            'dislikes': post.dislikes,
                            'img': post.images,
                            'tips': post.tips,
                            'created_at': post.created_at,
                            'created_by': user.name
                        }
                        post_contents.append(p)
                    # print(post_contents)
                    return jsonify({
                        'posts': post_contents
                    })
                else:
                    return "no post exit for this user", 404
        except:
            return "server error", 500

    def post(self):
        # print(bool(int(request.form['contain_image'])))
        contain_image = bool(int(request.form['contain_image']))
        v_user = Users.query.get(request.form['user_id'])
        if v_user:
            img = ''
            if contain_image:
                img = save_image(request.files['image'])
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            new_post = Posts(education=request.form['education'], user_id=request.form['user_id'],
                             img=img, likes=0, dislikes=0, title=request.form['title'], created_at=time)
            db.session.add(new_post)
            db.session.commit()
            return 'post successfully created', 201
        else:
            abort(400, message="enter a valid user id")

    def put(self):
        contain_image = bool(int(request.form['contain_image']))
        post = Posts.query.get(request.form['post_id'])
        if post:
            img = ''
            if contain_image:
                img = save_image(request.files['image'])
                post.img = img
            post.title = request.form['title']
            post.content = request.form['content']
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            post.time = time
            db.session.commit()
            return 'ok', 201
        else:
            abort(404, message="Post not found")

    def delete(self, post_id):
        post = Posts.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return 'deleted successfully', 201
        else:
            abort(404, message="no such post exists")


api.add_resource(Posts_api, '/api/posts',
                 '/api/<int:id>/posts/<int:user_id>', '/api/posts/<int:post_id>')


class Post_comment_api(Resource):
    def get(self, post_id, user_id):
        post = Posts.query.filter_by(post_id=post_id).first()
        user = Users.query.filter_by(user_id=user_id).first()
        if post and user:
            q = {
                'content': Post_comment.query.filter_by(post_id=post.post_id, user=user.user_id)
            }
            return jsonify(q)
        else:
            abort(404, message="no such post exists")

    def post(self):
        post_id, user_id = request.form['post_id'], request.form['user_id']
        user = Users.query.filter_by(user_id=user_id).first()
        post = Posts.query.filter_by(post_id=post_id).first()
        if user and post:
            comm = Post_comment(user_id=user_id, post_id=post_id)
            db.session.add(comm)
            db.session.commit()
        else:
            abort(404, message="worng credentials")

    def delete(self, post_id, user_id):
        comm = Post_comment.query.filter_by(
            user_id=user_id, post_id=post_id).first()
        if comm:
            db.session.delete(comm)
            db.session.commit()
            return 'comment deleted'
        else:
            abort(404, message="worng credentials")


api.add_resource(Post_comment_api, '/api/post_comm',
                 '/api/<int:post_id>/post_comm/<int:user_id>')


class Apti_api(Resource):
    def get(self, apti_id, user_id):
        user = Users.query.filter_by(user_id=user_id)
        if apti_id != 0:  # incase we want to fetch a particular post by user
            apti = Aptitude_test.query.filter_by(apti_id=apti_id).first()
            p = {
                'post_id': apti.id,
                'likes': apti.likes,
                'dislikes': apti.dislikes,
                'img': apti.images,
                'tips': apti.tips,
                'created_at': apti.created_at,
                'created_by': user.name
            }
            return jsonify(p)
        else:  # incase we want all the post from any particular user
            aptis = Aptitude_test.query.filter_by(created_by=user_id).all()
            # print(posts)
            if aptis:
                post_contents = []
                for apti in aptis:
                    p = {
                        'post_id': apti.id,
                        'likes': apti.likes,
                        'dislikes': apti.dislikes,
                        'img': apti.images,
                        'tips': apti.tips,
                        'created_at': apti.created_at,
                        'created_by': user.name
                    }
                    post_contents.append(p)
                # print(post_contents)
                return jsonify({
                    'posts': post_contents
                })
            else:
                return "no post exit for this user", 404

    def post(self):
        user_id = request.form['user_id']
        v_user = Users.query.get(user_id)
        if v_user:
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            new_post = Aptitude_test(education=request.form['education'], created_by=v_user.user_id,
                                     likes=0, dislikes=0, created_at=time)
            db.session.add(new_post)
            db.session.commit()
            return 'post successfully created', 201
        else:
            abort(400, message="enter a valid user id")

    def put(self):
        apti_id = request.form['apti_id']
        contain_image = bool(int(request.form['contain_image']))
        post = Aptitude_test.query.get(apti_id)
        if post:
            img = ''
            if contain_image:
                img = save_image(request.files['image'])
                post.img = img
            post.title = request.form['title']
            post.content = request.form['content']
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            post.time = time
            db.session.commit()
            return 'ok', 201
        else:
            abort(404, message="Post not found")

    def delete(self, apti_id):
        post = Aptitude_test.query.get(apti_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return 'deleted successfully', 201
        else:
            abort(404, message="no such post exists")


api.add_resource(Apti_api, '/apti/posts',
                 '/api/<int:apti_id>/apti/<int:user_id>', '/api/apti/<int:apti_id>')


class Apti_comment_api(Resource):
    def get(self, apti_id):
        comm = Apti_comment.query.filter_by(apti_id=apti_id).all()
        if comm:
            q = {
                'content': comm.content
            }
            return jsonify(q)
        else:
            abort(404, message="wrong credentials")

    def post(self):
        apti_id, user_id = request.form['apti_id'], request.form['user_id']
        apti = Aptitude_test.get(apti_id)
        user = Users.get(user_id)
        if apti and user:
            comm = Apti_comment(apti_id=apti_id, user_id=user_id)
            db.session.add(comm)
            db.session.commit()
            return 'comment added successfully', 201
        else:
            abort(404, message="wrong credentials")

    def delete(self, apti_id, user_id):
        comm = Apti_comment.query.filter_by(
            apti_id=apti_id, user_id=user_id).first()
        db.session.delete(comm)
        db.session.commit()


api.add_resource(Apti_comment_api, '/api/apti_comment',
                 '/api/<int:apti_id>/apti_comment/<int:user_id>', '/api/apti_comment/<int:user_id>')


class Test_question_api(Resource):
    def get(self, apti_id, quest_id):
        if quest_id != 0:  # incase we want to fetch a particular post by user
            quest = Test_quest.query.filter_by(
                quest_id=quest_id, apti_id=apti_id).first()
            q = {
                'question': quest.question,
                'type': quest.type
            }
            return jsonify(q)
        else:  # incase we want all the post from any particular user
            quests = Test_quest.query.filter_by(apti_id=apti_id).all()
            # print(posts)
            if quests:
                quests_contents = []
                for quest in quests:
                    p = {
                        'question': quest.question,
                        'type': quest.type
                    }
                    quests_contents.append(p)
                # print(post_contents)
                return jsonify({
                    'quests': quests_contents
                })
            else:
                return "no post exit for this user", 404

    def post(self):
        apti_id = request.form['apti_id']
        apti = Aptitude_test.query(apti_id=apti_id)
        if apti:
            new_quest = Test_quest(
                apti_id=apti_id, question=request.form['question'], type=request.form['type'])
            db.session.add(new_quest)
            db.session.commit()
            return 'question successfully created', 201
        else:
            abort(400, message="enter a valid aptitude id")

    def put(self):
        apti_id, quest_id = request.form['apti_id'], request.form['quest_id']
        quest = Test_quest.query(apti_id=apti_id, quest_id=quest_id).all()
        if quest:
            if request.form['question']:
                quest.question = request.form['question']
            if request.form['type']:
                quest.type = request.form['type']
            db.session.commit()
            return 'question successfully changed', 201
        else:
            abort(400, message="enter a valid aptitude id or question id")

    def delete(self, quest_id):
        quest = Test_quest.query.get(quest_id)
        if quest_id:
            db.session.delete(quest)
            db.session.commit()
            return 'deleted successfully', 201
        else:
            abort(404, message="no such question exists")


api.add_resource(Test_question_api, '/api/test_q',
                 '/api/<int:apti_id>/test_q/<int:quest_id>', '/api/test_q/<int:quest_id>')


class Test_score_api(Resource):
    def get(self, apti_id, user_id):
        new = Test_score.query.filter_by(
            apit_id=apti_id, user_id=user_id).first()
        if new:  # incase we want to fetch a particular post by user

            q = {
                'score': new.score
            }
            return jsonify(q)
        else:  # incase we want all the post from any particular user
            return "no post exit for this user", 404

    def post(self):
        apti_id, user_id = request.form['apti_id'], request.form['user_id']
        test = Aptitude_test.query.filter_by(apti_id=apti_id).first()
        user = Users.query.filter_by(user_id=user_id)
        if test and user:
            new_score = Test_score(
                apti_id=test.apti_id, user_id=user.user_id, score=request.form['score'])
            db.session.add(new_score)
            db.session.commit()
            return 'question successfully created', 201
        else:
            abort(400, message="enter a valid aptitude id")

    def put(self):
        apti_id, user_id = request.form['apti_id'], request.form['user_id']
        new = Test_score.query.filter_by(
            apit_id=apti_id, user_id=user_id).first()
        if new:
            if request.form['score']:
                new.score = request.form['score']
            return 'question successfully changed', 201
        else:
            abort(400, message="enter a valid aptitude id or user id")

    def delete(self, apti_id, user_id):
        new = Test_score.query.filter_by(
            apit_id=apti_id, user_id=user_id).first()
        if new:
            db.session.delete(new)
            db.session.commit()
            return 'deleted successfully', 201
        else:
            abort(404, message="no such question exists")


api.add_resource(Test_score_api, '/api/test_s',
                 '/api/<int:apti_id>/test_s/<int:user_id>')


class Answer_api(Resource):
    def get(self, quest_id):
        ans = Answers.query.filter_by(quest_id=quest_id).first()
        if ans:
            q = {
                'answers': ans.answers
            }
            return jsonify(q)
        else:
            abort(400, message='enter a valid question id')

    def post(self):
        quest_id = request.form['quest_id']
        quest = Test_quest.query.filter_by(quest_id=quest_id).first()
        if quest:
            ans = Answers(quest_id=quest_id)
            db.session.add(ans)
            db.session.commit()
            return 'anwer added successfully', 201
        else:
            abort(404, message="Eneter valid question id")

    def put(self):
        quest_id = request.form['quest_id']
        ans = Answers.query.filter_by(quest_id=quest_id).first()
        if ans:
            ans.answer = request.form['answer']
            return 'answer updated successfully ', 201
        else:
            abort(400, message='enter a valid question id')

    def delete(self, quest_id):
        ans = Answers.query.filter_by(quest_id=quest_id).first()
        if ans:
            db.session.delete(ans)
            db.session.commit()
            return 'deleted successfully'
        else:
            abort(400, message='enter a valid question id')


api.add_resource(Answer_api, '/api/ans', '/api/ans/<int:quest_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
