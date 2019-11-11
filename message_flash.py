from flask import Flask, redirect, render_template, url_for, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hw9823823hr3928299"
app.permanent_session_lifetime = timedelta(days=5)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        # form data 
        name = request.form["alias"]
        email = request.form["email"]
        passkey = request.form["password"]
        # Store formdata to session
        session["user"] = name
        flash("Login Successful")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("dashboard.html", user=user)
    else:
        flash("Sorry, you are not logged in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"you have been logged out, {user}", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
