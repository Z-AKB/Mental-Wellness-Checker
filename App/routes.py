from flask import Blueprint, render_template, request, redirect, url_for, session
from app import app
from logic import classify_wellness, calculate_scores

# Define the blueprint
app_routes = Blueprint('app_routes', __name__)

# Consent route
@app_routes.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        session["consent_given"] = True
        return redirect(url_for("app_routes.home"))  # Redirect to the home route after consent
    return render_template("consent.html")

# Home (questionnaire) route
@app_routes.route("/", methods=["GET", "POST"])
def home():
    # Check if consent is given before proceeding to the questionnaire
    if "consent_given" not in session or not session["consent_given"]:
        return redirect(url_for("app_routes.consent"))  # Redirect to consent page if not given

    if request.method == "POST":
        answers = request.form.to_dict()
        scores = calculate_scores(answers)
        classification = classify_wellness(scores)

        # Store the answers, scores, and classification in session
        session["answers"] = answers
        session["scores"] = scores
        session["classification"] = classification

        return redirect(url_for("app_routes.results"))

    return render_template("index.html")

# Results route
@app_routes.route("/results")
def results():
    if "scores" not in session:
        return redirect(url_for("app_routes.home"))  # Ensure there's data to display

    scores = session.get("scores")
    classification = session.get("classification")
    return render_template("results.html", scores=scores, classification=classification)

# Optionally, you can also handle the 'index' route logic here if you still want that
@app_routes.route("/index", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        total_score = sum(int(request.form.get(f"q{i}")) for i in range(1, 6))
        if total_score <= 3:
            result = "You appear to be doing well. Keep taking care of your mental health!"
        elif total_score <= 6:
            result = "You're experiencing mild stress. Consider incorporating self-care practices."
        elif total_score <= 9:
            result = "You may be moderately struggling. Talking to someone or seeking support may help."
        else:
            result = "You might be going through significant stress. It's important to seek professional help."
    return render_template("index.html", result=result)
