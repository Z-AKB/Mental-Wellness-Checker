from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for encrypting session data

# Route to collect consent
@app.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        session["consent_given"] = True  # Store consent in session
        return redirect(url_for("home"))
    return render_template("consent.html")

# Home route (questionnaire)
@app.route("/", methods=["GET", "POST"])
def home():
    # Check if consent is given before showing the questionnaire
    if "consent_given" not in session or not session["consent_given"]:
        return redirect(url_for("consent"))  # Redirect to consent page if not given

    if request.method == "POST":
        # Process the form data
        answers = request.form
        # Example: Process answers (calculate score, etc.)
        score = sum(int(answers.get(f"question{i}")) for i in range(1, 3))  # Summing the answers for example
        classification = classify_wellness(score)

        # Store data temporarily in session (ensure it’s not permanent)
        session["answers"] = answers
        session["score"] = score
        session["classification"] = classification

        return redirect(url_for("results"))

    return render_template("index.html")

# Results route
@app.route("/results")
def results():
    # Ensure that there is a score to display
    if "score" not in session:
        return redirect(url_for("home"))  # Ensure there's a score to display

    score = session.get("score")
    classification = session.get("classification")
    return render_template("results.html", score=score, classification=classification)

def classify_wellness(score):
    if score <= 5:
        return "Excellent"
    elif 6 <= score <= 10:
        return "Good"
    elif 11 <= score <= 15:
        return "Fair"
    else:
        return "Poor"

if __name__ == "__main__":
    app.run(debug=True)
