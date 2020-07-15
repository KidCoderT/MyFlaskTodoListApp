from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean)

@app.route('/')
def index():
    incomplete_todos = Todo.query.filter_by(completed=False).all()
    return render_template("index.html", unfinished_todos=incomplete_todos)

@app.route('/add', methods=["POST"])
def add():
    new_todo = Todo(text=request.form["todoitem"], completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/completed/<id>', methods=["POST"])
def completed():
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.completed = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/uncheck/<id>', methods=["POST"])
def uncheck():
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.completed = False
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<id>', methods=["POST"])
def uncheck():
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
