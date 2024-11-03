import uuid
from flask import Flask, abort, flash, request, render_template, redirect, url_for
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
from random import randint
import os
import base64
import werkzeug

from .db import get_db, close_db
from . import ai

load_dotenv()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.teardown_appcontext(close_db)

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
)

checkpoint = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
device = "cuda"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)


# function taken from flask docs
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get-to-know-you/", methods=("GET", "POST"))
def form():
    if request.method == "POST":
        error = False

        try:
            name_1 = request.form["ID1"]
            occupation1 = request.form["occupation1"]
            feed1 = request.files["feed1"]

            name_2 = request.form["ID2"]
            occupation2 = request.form["occupation2"]
            feed2 = request.files["feed2"]

        except werkzeug.exceptions.BadRequestKeyError:
            flash("Required field wasn't provided")
            error = True
        else:
            if not allowed_file(feed1.filename) or not allowed_file(feed2.filename):
                flash("File not of allowed type!")
                error = True

        if not error:
            feed1_b64 = base64.b64encode(feed1.read())
            feed2_b64 = base64.b64encode(feed2.read())

            # TODO: DO ALL AI PROCESSING HERE (match_score just randomly generated at the moment)
            # TODO: GET DATA FROM IMAGE

            # TODO: CALCULATE MATCH SCORE
            # FEED IN DATA FROM IMAGE INTO QUERY

            ###### TEMPORARY RANDOM GENERATION ########
            match_score = randint(1, 100)
            ##########################################

            db = get_db()
            result_id = str(uuid.uuid4())
            db.execute(
                "INSERT INTO result VALUES (?, ?, ?, ?)",
                (result_id, name_1, name_2, match_score),
            )
            db.commit()
            app.logger.info(
                f"INSERTED INTO result: {result_id}, {name_1}, {name_2}, {match_score}"
            )

            return redirect(url_for("result", result_id=result_id), code=302)

    return render_template("form.html")


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


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", status_code=404), 404


# DEVELOPER NOTE: I WANT PIZZA!
