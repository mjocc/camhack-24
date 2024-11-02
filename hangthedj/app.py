from flask import Flask, abort, request, render_template, redirect, url_for
from dotenv import load_dotenv
import os

from .db import get_db, close_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.teardown_appcontext(close_db)


@app.route("/result/<uuid:result_id>")
def result(result_id):
    db = get_db()
    result = db.execute(
        "SELECT * FROM result WHERE uuid = ?",
        (
            str(
                result_id,
            ),
        ),
    ).fetchone()

    if result is None:
        abort(404)

    return render_template("results.html", result=result)


@app.route("/")
def home():
    return render_template("index.html")
