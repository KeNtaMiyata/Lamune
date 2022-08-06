from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os
import pytz


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lamune.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config["TEMPLATES_AUTO_RELOAD"] = True          # Ensure templates are auto-reloaded

db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    problems = db.relationship('Problem', backref='user', lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    stage =  db.Column(db.Integer, default=0)
    last_time = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route('/', methods=["GET"])
def index():
    problems=Problem.query.all()
    return render_template("index.html", problems=problems)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        
        # check blank or not
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirm"):
            return apology("must provide password", 403)

        name = request.form.get("name")
        password = request.form.get("password")
        confirm = request.form.get("confirm")


        return redirect("/login")
    
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route('/new', methods=["GET", "POST"])
def new():
    if request.method == "POST":

        title = request.form.get("title")
        body = request.form.get("body")
        answer = request.form.get("answer")

        problem = Problem(title=title, body=body, answer=answer)

        db.session.add(problem)
        db.session.commit()

        return redirect("/")

    else:
        return render_template("new.html")

@app.route('/<int:id>/update', methods=["GET", "POST"])
def update(id):
    problem=Problem.query.get(id)

    if request.method == "POST":
        problem.title = request.form.get("title")
        problem.body = request.form.get("body")
        problem.answer = request.form.get("answer")
        
        db.session.commit()

        return redirect("/")

    else:
        return render_template("update.html", problem=problem)

@app.route('/<int:id>/delete',methods=["GET"])
def delete(id):
    problem=Problem.query.get(id)
    db.session.delete(problem)
    db.session.commit()
    return redirect("/")