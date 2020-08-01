from myapp import app, db
from myapp.models import Todo, User
from flask import render_template, request, redirect, url_for, flash, session

# All the views
@app.route('/')
@app.route('/home')
def home():
    session['redirect_to'] = "mytodos"
    if session.get("user_name"):
        return redirect(url_for("mytodos"))
    return render_template("home.html")

@app.route('/mytodos')
def mytodos():
    if session.get("user_name"):
        incomplete_todos = Todo.query.filter_by(completed=False, user_id=session.get("user_id")).all()
        completed_todos = Todo.query.filter_by(completed=True, user_id=session.get("user_id")).all()
        return render_template("todos.html", unfinished_todos=incomplete_todos, finished_todos=completed_todos)
    flash("Please Login to continue!!", category="error")
    session['redirect_to'] = "mytodos"
    return redirect(url_for("login"))

@app.route('/mytodos/add', methods=["POST", "GET"])
def add():
    if session.get("user_name"):
        new_todo = Todo(text=request.form["todoitem"], completed=False, user_id=session.get("user_id"))
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    session['redirect_to'] = "mytodos"
    return redirect(url_for("login"))

@app.route('/mytodos/completed/<id>')
def completed(id):
    if session.get("user_name"):
        todo = Todo.query.filter_by(id=int(id), user_id=session.get("user_id")).first().completed = True
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    session['redirect_to'] = "mytodos"
    return redirect(url_for("login"))

@app.route('/mytodos/uncheck/<id>')
def uncheck(id):
    if session.get("user_name"):
        todo = Todo.query.filter_by(id=int(id), user_id=session.get("user_id")).first().completed = False
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    session['redirect_to'] = "mytodos"
    return redirect(url_for("login"))

@app.route('/mytodos/delete/<id>')
def delete(id):
    if session.get("user_name"):
        todo = Todo.query.filter_by(id=int(id), user_id=session.get("user_id")).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("mytodos"))
    flash("Please Login to continue!!", category="error")
    session['redirect_to'] = "mytodos"
    return redirect(url_for("login"))

@app.route('/user/login', methods=["POST", "GET"])
def login():
    if session.get("user_name"):
        flash(f"You are already logged there is no need to login again {session.get('user_name')}", category="success")
        return redirect(url_for("user_profile"))

    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user:
            if user.get_password(request.form.get("password")):
                flash(f"You were successfully Logged in!! Welcome back {user.name.title()}!!", category="success")
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_image'] = user.profile_image
                if session.get("redirect_to") == "user_profile":
                    return redirect(url_for(session.get("redirect_to"), name=session.get('user_name')))
                return redirect(url_for(session.get("redirect_to")))
            else:
                flash("Sorry but there was some error!!", category="error")
                return render_template("login.html")
        else:
            flash("there was some error!!", category="error")
            email_error = True
            password_error = False
            return render_template("login.html", email_error=email_error, email=request.form.get("email"), password_error=password_error)
    return render_template("login.html")

@app.route('/user/signup', methods=["POST", "GET"])
def signup():
    if session.get("user_name"):
        flash(f"You are already a user {session.get('user_name')}. You need to logout if you want to create a new account!!", category="success")
        return redirect(url_for("mytodos"))

    if request.method == "POST":

        form_return_data = [request.form.get("username"), request.form.get("email"), request.form.get("password"), request.form.get("repeatpassword")]

        email_list = []
        for i in User.query.all():
            email_list.append(i.get("email"))

        if request.form.get("email") not in email_list:
            if request.form.get("password") == request.form.get("repeatpassword"):

                user_list = []
                for i in User.query.all():
                    user_list.append(i.get("name"))

                if request.form.get("username") not in user_list:
                    try:
                        new_user = User(name=request.form.get("username"), email=request.form.get("email"), password="")
                        new_user.set_password(request.form.get("password"))
                        db.session.add(new_user)
                        db.session.commit()
                        session['redirect_to'] = "home"
                        return redirect(url_for("login"))
                    except Exception as e:
                        print(e)
                        flash("some error happened while trying to create your User Model!! Try Again", category="model")
                else:
                    flash("your username is already taken!!", category="user")
            else:
                flash("there was some error in your password!!", category="error")
                flash("your passwords don't match!!", category="password")

        else:
            flash("Sorry but there was some error with your email!!", category="error")

        return render_template("signup.html", form_data=form_return_data)

    return render_template("signup.html")

@app.route('/user/logout')
def logout():
    session["user_id"] = False
    session.pop("user_name", False)
    session.pop("user_image", None)
    session['redirect_to'] = "mytodos"
    return redirect(url_for("home"))

@app.route('/<name>/profile')
def user_profile(name):
    if session.get("user_name"):
        if session.get("user_name") == name:
            return render_template("user_profile.html")
        else:
            flash("You cant go to others profile !!")
            return redirect(url_for("user_profile", name=session.get("user_name")))
    flash("Please Login to continue!!", category="error")
    session['redirect_to'] = "user_profile"
    return redirect(url_for("login"))

