from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os
import pytz


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lamune.db'
app.config['SECRET_KEY'] = os.urandom(24)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)

login_manager = LoginManager()
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
    stage = db.Column(db.Integer, default=0)
    last_time = db.Column(db.DateTime, nullable=False,
                          default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route("/", methods=["GET"])
def top():
    return render_template("top.html")


@app.route("/index", methods=["GET"])
@login_required
def index():
    problems = Problem.query.all()
    return render_template("index.html", problems=problems)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        # check blank or not
        if not request.form.get("username"):
            return redirect("/signup")
            # return apology("must provide username", 403)

        elif not request.form.get("password"):
            return redirect("/signup")
            # return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return redirect("/signup")
            # return apology("must provide password", 403)

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return redirect("/signup")
            # return apology("Password and confirmation are not same", 400)

        users = User.query.all()
        if name in [person.name for person in users]:
            return redirect("/signup")
            # return apology("The name is already used by someone", 400)

        user = User(name=name, password=generate_password_hash(
            password, method="sha256"))

        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # check blank or not
        if not request.form.get("username"):
            print(1)
            return redirect("/signup")
            # return apology("must provide username", 403)

        elif not request.form.get("password"):
            print(2)
            return redirect("/signup")
            # return apology("must provide password", 403)

        name = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(name=name).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect("/index")

        return redirect("/login")

    else:
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/new', methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":

        if not request.form.get("title"):
            print(1)
            return redirect("/new")

        elif not request.form.get("body"):
            print(2)
            return redirect("/new")

        elif not request.form.get("answer"):
            print(3)
            return redirect("/new")

        user_id = current_user.id
        title = request.form.get("title")
        body = request.form.get("body")
        answer = request.form.get("answer")

        problem = Problem(user_id=user_id, title=title,
                          body=body, answer=answer)

        db.session.add(problem)
        db.session.commit()

        return redirect("/index")

    else:
        return render_template("new.html")


@app.route('/<int:id>/update', methods=["GET", "POST"])
@login_required
def update(id):
    problem = Problem.query.get(id)

    if request.method == "POST":
        problem.title = request.form.get("title")
        problem.body = request.form.get("body")
        problem.answer = request.form.get("answer")

        db.session.commit()

        return redirect("/index")

    else:
        return render_template("update.html", problem=problem)


@app.route('/<int:id>/delete', methods=["GET"])
@login_required
def delete(id):
    problem = Problem.query.get(id)
    db.session.delete(problem)
    db.session.commit()
    return redirect("/index")
