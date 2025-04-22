from flask import render_template, request, redirect, url_for, session
from app import app
from logic import classify_wellness, calculate_scores

# Consent route
@app.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        session["consent_given"] = True
        return redirect(url_for("home"))
    return render_template("consent.html")

# Home (questionnaire) route
@app.route("/", methods=["GET", "POST"])
def home():
    if "consent_given" not in session or not session["consent_given"]:
        return redirect(url_for("consent"))

    if request.method == "POST":
        answers = request.form.to_dict()
        scores = calculate_scores(answers)
        classification = classify_wellness(scores)

        session["answers"] = answers
        session["scores"] = scores
        session["classification"] = classification

        return redirect(url_for("results"))

    return render_template("index.html")

# Results route
@app.route("/results")
def results():
    if "scores" not in session:
        return redirect(url_for("home"))

    scores = session.get("scores")
    classification = session.get("classification")
    return render_template("results.html", scores=scores, classification=classification)
