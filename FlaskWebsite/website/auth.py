from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ["GET", "POST"])
def login():
    return render_template("login.html", text="Testing", user = "Tim")

@auth.route('/logout')
def logout():
    return "<p>Logout</p1>"

@auth.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4:
            flash("Email must be valid", category = "error")
        elif len(firstName) < 2:
            flash("First name must be greater than one character", category = "error")
        elif password1 != password2:
            flash("Passwords do not match!", category = "error")
        elif len(password1) < 5:
            flash("Password must be more than 5 characters! ", category = "error")
        else:
            # add user to database
            flash("Account created!", category = "success")
            pass

    return render_template("sign_up.html")