from flask import Flask, request, render_template, flash, g, session, redirect, url_for

app = Flask(__name__)

app.config.from_object('config')

@app.route("/")
def hello_world():
    return render_template("hello.html", name=__name__)
