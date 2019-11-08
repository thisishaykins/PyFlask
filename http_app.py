from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["alias"]
        # email = request.form["email"]
        # passkey = request.form["password"]
        return redirect(url_for("user", usr=name))
    else:
        return render_template("login.html")


@app.route("/<usr>")
def user(usr):
    return render_template("dashboard.html", user=usr)


if __name__ == "__main__":
    app.run(debug=True)
