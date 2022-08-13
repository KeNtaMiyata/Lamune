from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import os
import pytz
from helpers import apology, show_datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lamune.db'
app.config['SECRET_KEY'] = os.urandom(24)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.filters["show_datetime"] = show_datetime

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# models


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
                          default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
    solved_history = db.Column(db.String)


# stage passed time list
stage_list = [
    datetime.timedelta(seconds=1),
    datetime.timedelta(seconds=15),
    datetime.timedelta(seconds=15),
    datetime.timedelta(seconds=20),
    # datetime.timedelta(hours=3),
    # datetime.timedelta(days=1),
    # datetime.timedelta(days=3),
    # datetime.timedelta(days=7),
    # datetime.timedelta(days=10),
    # datetime.timedelta(days=15),
    # datetime.timedelta(days=20),
    # datetime.timedelta(days=30)
]

max_stage = len(stage_list) - 1

# routing


@app.route("/", methods=["GET"])
def top():
    return render_template("top.html", user=current_user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        # check blank or not
        if not request.form.get("username"):
            # return redirect("/signup")
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            # return redirect("/signup")
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            # return redirect("/signup")
            return apology("must provide password", 403)

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            # return redirect("/signup")
            return apology("Password and confirmation are not same", 400)

        users = User.query.all()
        if name in [person.name for person in users]:
            # return redirect("/signup")
            return apology("The name is already used by someone", 400)

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
            # return redirect("/signup")
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            print(2)
            # return redirect("/signup")
            return apology("must provide password", 403)

        name = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(name=name).first()
        if not user:
            return apology("must provide valid username", 403)

        if check_password_hash(user.password, password):
            login_user(user)
            user_id = user.id
            return redirect(f"/{ user_id }/index")

        return apology("foo", 403)

    else:
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/<int:user_id>/index", methods=["GET"])
@login_required
def index(user_id):
    my_problems = Problem.query.filter_by(user_id=user_id).all()
    user = current_user
    return render_template("index.html", problems=my_problems, user=user)


@app.route('/<int:user_id>/new', methods=["GET", "POST"])
@login_required
def new(user_id):
    if request.method == "POST":

        if not request.form.get("title"):
            print(1)
            return apology("foo", 403)

        elif not request.form.get("body"):
            print(2)
            return apology("foo", 403)

        elif not request.form.get("answer"):
            print(3)
            return apology("foo", 403)

        # user_id = current_user.id
        title = request.form.get("title")
        body = request.form.get("body")
        answer = request.form.get("answer")

        problem = Problem(user_id=user_id, title=title,
                          body=body, answer=answer)

        db.session.add(problem)
        db.session.commit()

        return redirect(f"/{ user_id }/index")

    else:
        user = current_user
        return render_template("new.html", user=user)


@app.route('/<int:user_id>/<int:problem_id>', methods=["GET"])
@login_required
def show(user_id, problem_id):
    problem = Problem.query.get(problem_id)
    user = current_user
    if problem.solved_history:
        history_list=problem.solved_history.splitlines()
    else:
        history_list=[]
    return render_template("show.html", problem=problem, user=user, history_list=history_list)


@app.route('/<int:user_id>/<int:problem_id>/update', methods=["GET", "POST"])
@login_required
def update(user_id, problem_id):
    problem = Problem.query.get(problem_id)

    if request.method == "POST":

        if not request.form.get("title"):
            print(1)
            return apology("foo", 403)

        elif not request.form.get("body"):
            print(2)
            return apology("foo", 403)

        elif not request.form.get("answer"):
            print(3)
            return apology("foo", 403)

        problem.title = request.form.get("title")
        problem.body = request.form.get("body")
        problem.answer = request.form.get("answer")

        db.session.commit()

        return redirect(f"/{ user_id }/index")

    else:
        user = current_user
        return render_template("update.html", problem=problem, user=user)


@app.route('/<int:user_id>/<int:problem_id>/delete', methods=["GET"])
@login_required
def delete(user_id, problem_id):
    problem = Problem.query.get(problem_id)
    db.session.delete(problem)
    db.session.commit()
    return redirect(f"/{ user_id }/index")


@app.route('/<int:user_id>/<int:problem_id>/trytry', methods=["GET", "POST"])
@login_required
def trytry(user_id, problem_id):
    if request.method == "POST":
        problem = Problem.query.get(problem_id)
        problem.last_time = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        result = request.form.get("result")

        if result == "Correct":
            if not problem.solved_history:
                problem.solved_history = f"{show_datetime(datetime.datetime.now(pytz.timezone('Asia/Tokyo')))},Correct"
            else:
                problem.solved_history = f"{show_datetime(datetime.datetime.now(pytz.timezone('Asia/Tokyo')))},Correct\n{problem.solved_history}"

            if problem.stage != max_stage:
                problem.stage += 1
            db.session.commit()

        else:
            if not problem.solved_history:
                problem.solved_history = f"{show_datetime(datetime.datetime.now(pytz.timezone('Asia/Tokyo')))},Incorrect"
            else:
                problem.solved_history = f"{show_datetime(datetime.datetime.now(pytz.timezone('Asia/Tokyo')))},Incorrect\n{problem.solved_history}"

            problem.stage = 0
            db.session.commit()

        return redirect(f"/{user_id}/tasks")

    else:
        problem = Problem.query.get(problem_id)
        return render_template("trytry.html", problem=problem, user=current_user)


@app.route("/<int:user_id>/tasks", methods=["GET"])
@login_required
def tasks(user_id):
    tasks = []
    my_problems = Problem.query.filter_by(user_id=user_id).all()

    for problem in my_problems:

        passed_time = datetime.datetime.now(pytz.timezone(
            'Asia/Tokyo')).replace(tzinfo=None) - problem.last_time

        if passed_time >= stage_list[problem.stage]:
            tasks.append(problem)

        else:
            continue

    return render_template("tasks.html", problems=tasks, user=current_user)
