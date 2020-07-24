from myapp import app, db
from myapp.models import Todo, User
from flask import Flask, render_template, request, redirect, url_for, flash, session

@app.route('/')
@app.route('/home')
def home():
    if session.get("user_name"):
        return render_template("user_home.html")
    return render_template("user_home.html", name="Tejas", email="Tejas75O25@gmail.com")

@app.route('/mytodos')
def mytodos():
    if session.get("user_name"):
        incomplete_todos = Todo.query.filter_by(completed=False, user_id=session.get("user_id")).all()
        completed_todos = Todo.query.filter_by(completed=True, user_id=session.get("user_id")).all()
        return render_template("todos.html", unfinished_todos=incomplete_todos, un_todos_len=len(incomplete_todos), finished_todos=completed_todos, fin_todos_len=len(completed_todos))
    flash("Please Login to continue!!", category="error")
    return redirect(url_for("login"))

@app.route('/mytodos/add', methods=["POST", "GET"])
def add():
    if session.get("user_name"):
        new_todo = Todo(text=request.form["todoitem"], completed=False, user_id=session.get("user_id"))
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    return redirect(url_for("login"))

@app.route('/mytodos/completed/<id>')
def completed(id):
    if session.get("user_name"):
        todo = Todo.query.filter_by(id=int(id), user_id=session.get("user_id")).first()
        todo.completed = True
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    return redirect(url_for("login"))

@app.route('/mytodos/uncheck/<id>')
def uncheck(id):
    if session.get("user_name"):
        todo = Todo.query.filter_by(id=int(id), user_id=session.get("user_id")).first()
        todo.completed = False
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    return redirect(url_for("login"))

@app.route('/mytodos/delete/<id>')
def delete(id):
    if session.get("user_name"):
        todo = Todo.query.filter_by(id=int(id), user_id=session.get("user_id")).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    return redirect(url_for("login"))

@app.route('/user/login', methods=["POST", "GET"])
def login():
    if session.get("user_name"):
        flash("You are aldready logged there is no need to login again {}".format(session.get("user_name")), category="success")
        return redirect(url_for("mytodos"))

    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user:
            if user.get_password(request.form.get("password")):
                flash("You were successfullyy Logged in!! Welcome back {}!!".format(user.name.title()), category="success")
                session['user_id'] = user.id
                session['user_name'] = user.name
                return redirect(url_for("mytodos"))
        else:
            flash("there was some error!!", category="error")
            email_error = True
            password_error = False
            return render_template("login.html", email_error=email_error, email=request.form.get("email"), password_error=password_error)
    return render_template("login.html")

@app.route('/user/signup', methods=["POST", "GET"])
def signup():
    if session.get("user_name"):
        flash("You are aldready a user {}. You need to loggout if you want to create a new account!!".format(session.get("user_name")), category="success")
        return redirect(url_for("mytodos"))

    if request.method == "POST":

        form_return_data = [request.form.get("username"), request.form.get("email"), request.form.get("password"), request.form.get("repeatpassword")]
        
        email_list = []
        for i in User.query.all():   
            email_list.append(i.__dict__["email"])

        if request.form.get("email") not in email_list:
            if request.form.get("password") == request.form.get("repeatpassword"):

                user_list = []
                for i in User.query.all():   
                    user_list.append(i.__dict__["name"])
                
                if request.form.get("username") not in user_list:
                    try:
                        new_user = User(name=request.form.get("username"), email=request.form.get("email"), password="")
                        new_user.set_password(request.form.get("password"))
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for("login"))
                    except Exception as e:
                        flash("some error happened while trying to create your User Model!! Try Again", category="model")
                else:
                    flash("your username is aldready taken!!", category="user")
            else:
                flash("there was some error in your password!!", category="error")
                flash("your passwords don't match!!", category="password")
                email_error = False
                password_error = True
        
        else:
            flash("Sorry but there was some error with your email!!", category="error")
            flash("Sorry but your email has aldready been taken!!", category="email")
            email_error = True
            password_error = False

        return render_template("signup.html", form_data=form_return_data)
    
    return render_template("signup.html")

@app.route('/user/logout')
def logout():
    session["user_id"] = None
    session.pop("user_name", None)
    return redirect(url_for("home"))

@app.route('/send_email', methods=["POST", "GET"])
def send_email():
  flash("Your email has been sent 🙂", category="success")
  return redirect("home")
