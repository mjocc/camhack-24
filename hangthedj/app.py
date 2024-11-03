import uuid
from flask import Flask, abort, flash, request, render_template, redirect, url_for
from dotenv import load_dotenv
from random import randint
import os
import base64
import werkzeug
import random
import time

# hello there
load_dotenv()

from .db import get_db, close_db
from . import ai


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
SITUATIONS = [
    "long hot car ride",
    "first meeting",
    "assembling IKEA furniture",
    "drunk fight",
    "losing something valuable",
    "married for 3 years",
]

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.teardown_appcontext(close_db)


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

            parameters1 = ai.classify_image(feed1_b64)
            parameters2 = ai.classify_image(feed2_b64)
            p1_attributes = parameters1.choices[0].message.content
            p2_attributes = parameters2.choices[0].message.content

            loading_screen1 = ai.generate_dialogue(
                name_1,
                name_2,
                p1_attributes,
                p2_attributes,
                occupation1,
                occupation2,
                SITUATIONS[random.randint(0, 2)],
            )
            loading_screen1 = loading_screen1[: loading_screen1.rfind(".") + 1]
            loading_screen2 = ai.generate_dialogue(
                name_1,
                name_2,
                p1_attributes,
                p2_attributes,
                occupation1,
                occupation2,
                SITUATIONS[random.randint(3, 5)],
            )
            loading_screen2 = loading_screen2[: loading_screen2.rfind(".") + 1]

            db = get_db()
            result_id = str(uuid.uuid4())
            db.execute(
                "INSERT INTO result (uuid, name_1, name_2, name_1_desc, name_2_desc, name_1_occupation, name_2_occupation, loading_screen_1, loading_screen_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    result_id,
                    name_1,
                    name_2,
                    p1_attributes,
                    p2_attributes,
                    occupation1,
                    occupation2,
                    loading_screen1,
                    loading_screen2,
                ),
            )
            db.commit()
            app.logger.info(
                f"INSERTED INTO result: {result_id}, {name_1}, {name_2}, etc."
            )

            return redirect(
                url_for("loading", result_id=result_id),
                code=302,
            )

    return render_template("form.html")


@app.route("/loading/<uuid:result_id>")
def loading(result_id):
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

    return render_template("loading.html", result=result)


@app.route("/ping")
def ping():
    return "I'm up!"


@app.route("/calculate-match/<uuid:result_id>")
def calculate_match(result_id):
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

    percentage_list = []
    for i in range(len(SITUATIONS)):
        print(f"RUNNING SITUATION: {SITUATIONS[i]}")
        percentage_list.append(
            ai.run_scenario(
                result["name_1"],
                result["name_2"],
                result["name_1_desc"],
                result["name_2_desc"],
                result["name_1_occupation"],
                result["name_2_occupation"],
                SITUATIONS[i],
            )
        )
    avg_p = sum(percentage_list) / len(percentage_list)
    percentage_dict = dict(zip(SITUATIONS, percentage_list))

    db = get_db()
    db.execute(
        """UPDATE result
        SET match_score = ?,
            car_score = ?,
            meeting_score = ?,
            ikea_score = ?,
            fight_score = ?,
            losing_score = ?,
            marriage_score = ?
        WHERE uuid = ?""",
        (
            avg_p,
            percentage_dict["long hot car ride"],
            percentage_dict["first meeting"],
            percentage_dict["assembling IKEA furniture"],
            percentage_dict["drunk fight"],
            percentage_dict["losing something valuable"],
            percentage_dict["married for 3 years"],
            str(
                result_id,
            ),
        ),
    )
    db.commit()

    return {"ok": True}


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


@app.errorhandler(500)
def not_found(e):
    return render_template("error.html", status_code=500), 500


@app.errorhandler(400)
def not_found(e):
    return render_template("error.html", status_code=400), 400


# DEVELOPER NOTE: I WANT PIZZA! update! we got pizza!!!
