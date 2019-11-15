from flask import Flask, redirect, render_template, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hw9823823hr3928299"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=5)

# Database Objes
db = SQLAlchemy(app)

class users(db.Model):
    _id     = db.Column("id", db.Integer, primary_key=True)
    name    = db.Column("name", db.String(100))
    email   = db.Column("email", db.String(100))
    phone   = db.Column("phone", db.String(100))
    passkey = db.Column("password", db.String(100))

    def __init__(self, name, email, phone, passkey):
        self.name = name
        self.email = email
        self.phone = phone
        self.passkey = passkey


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/view-users")
def view_users():
    email = request.args.get("delete_email")
    if email:
        delete_user = users.query.filter_by(email=email).delete()
        db.session.commit()
        if delete_user:
            flash("Account has been deleted")
        else:
            flash(f"Sorry, unable to delete account with the email {email}")

    return render_template("users.html", users=users.query.all())


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.permanent = True
        # form data 
        name = request.form["alias"]
        email = request.form["email"]
        phone = request.form["phone"]
        passkey = request.form["password"]

        # Store formdata to session
        # session["email"] = email

        found_user = users.query.filter_by(email=email).first()
        if found_user:
            flash("Sorry an account exist with email... Kindly proceed to Login")
        else:
            usr = users(name, email, phone, passkey)
            db.session.add(usr)
            db.session.commit()

            flash("Account Successful created. Kindly proceed with Login")
            return redirect(url_for("login"))
    else:
        if "email" in session:
            flash("Already Logged In!")
            return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        # form data 
        email = request.form["email"]
        passkey = request.form["password"]

        found_user = users.query.filter_by(email=email, passkey=passkey).first()
        if found_user:
            session["email"] = found_user.email
            flash("Login Successful")
            return redirect(url_for("profile"))
        else:
            flash("Sorry, email or password is incorrect. Thank you")
            # return render_template("login.html")

    else:
        if "email" in session:
            flash("Already Logged In!")
            return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    email = None
    if "email" in session:
        email = session["email"]
        found_user = users.query.filter_by(email=email).first()

        if request.method == "POST":
            name = request.form["alias"]
            phone = request.form["phone"]

            pulled_user = users.query.filter_by(email=email).first()
            pulled_user.name = name
            pulled_user.phone = phone
            db.session.commit()

            flash("Account Successful updated. Cheers")

        return render_template("profile.html", profile=found_user)
    else:
        flash("Sorry, you are not logged in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "email" in session:
        email = session["email"]
        flash(f"you have been successfuly logged out,", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
