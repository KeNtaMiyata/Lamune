from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lamune.db'
db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    stage =  db.Column(db.Integer, default=0)
    last_time = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route('/', methods=["GET"])
def index():
    problems=Problem.query.all()
    return render_template("index.html", problems=problems)

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


