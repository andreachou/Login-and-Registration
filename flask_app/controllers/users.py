from codecs import register_error
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def log_and_reg():
    return render_template("log_and_reg.html")



@app.route("/login", methods=["POST"])
def login():
    #Validate login form
    if not User.validate_login(request.form):
        return redirect("/")
    
    user = User.get_user_by_email(request.form)

    #check if user exists
    if user:
        # if user exists, check if password matches
        if not bcrypt.check_password_hash(user.password, request.form["password"]):
            # if password did not match
            flash("Email/Password combination is incorrect")
            return redirect("/")
    
        #if password matched
        session['user_id'] = user.id
        flash("Login was successful!")
        return redirect("/dashboard")

    # return user to form with validations
    flash("Email is not tied to an account")
    return redirect("/")



@app.route("/register", methods=["POST"])
def register():
    #Validate register form
    if not User.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    register_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    user_id = User.register_user(register_data)
    session["user_id"] = user_id
    flash("Registration was successful")
    return redirect("/dashboard")



@app.route("/dashboard")
def user_dashboard():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template("dashboard.html", user=user)
    # left hand side user is a variable that will be reference in the dashboard.html, and the right hand side user is whatever the value is for variable.



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")