from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import os

from .db import get_db, close_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.teardown_appcontext(close_db)


@app.route("/testing")
def testing():
    db = get_db()
    db.execute(
        "SELECT * FROM result WHERE uuid = ?",
    )
    return render_template("index copy.html")


@app.route("/")
def home():
    return render_template("index.html")
