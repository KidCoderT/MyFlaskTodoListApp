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

    def __str__(self):
        return self.text

@app.route('/')
def index():
    incomplete_todos = Todo.query.filter_by(completed=False).all()
    completed_todos = Todo.query.filter_by(completed=True).all()
    return render_template("index.html", unfinished_todos=incomplete_todos, finished_todos=completed_todos)

@app.route('/add', methods=["POST"])
def add():
    new_todo = Todo(text=request.form["todoitem"], completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/completed/<id>')
def completed(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.completed = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/uncheck/<id>')
def uncheck(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.completed = False
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<id>')
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
