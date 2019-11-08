from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/page/<name>")
def page(name):
    return render_template("index.html", content = name, r = 2, users = ["Akin", "Samuel", "Bill"])


if __name__ == "__main__":
    app.run(debug=True)
