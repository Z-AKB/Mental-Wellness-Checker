import sqlite3
import os
import matplotlib.pyplot as plt
import io
import base64

DATABASE = 'mental_wellness.db'

# Clinical thresholds for classification
clinical_thresholds = {
    'Stress': [0, 5, 10, 15],
    'Anxiety': [0, 4, 8, 12],
    'Depression': [0, 6, 12, 18]
}

def classify_wellness(scores):
    interpretation = {}
    for dimension, score in scores.items():
        thresholds = clinical_thresholds[dimension]
        if score <= thresholds[1]:
            level = "Low"
        elif score <= thresholds[2]:
            level = "Moderate"
        else:
            level = "High"
        interpretation[dimension] = level
    return interpretation

def plot_scores(scores):
    fig, ax = plt.subplots()
    ax.bar(scores.keys(), scores.values(), color=['blue', 'orange', 'green'])
    ax.set_title('Mental Wellness Scores')
    ax.set_ylabel('Score')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

# Database Initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            dimension TEXT NOT NULL,
            score_1 INTEGER,
            score_2 INTEGER,
            score_3 INTEGER,
            score_4 INTEGER,
            score_5 INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Scoring System
def calculate_scores(responses):
    scores = {'Stress': 0, 'Anxiety': 0, 'Depression': 0}
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for key, value in responses.items():
        cursor.execute("SELECT dimension, score_1, score_2, score_3, score_4, score_5 FROM questions WHERE id=?", (key,))
        q = cursor.fetchone()
        if q:
            dimension, *scales = q
            score = scales[int(value) - 1]
            scores[dimension] += score
    conn.close()
    return scores

# Threshold Classification
def classify_scores(scores):
    classifications = {}
    for dimension, score in scores.items():
        thresholds = clinical_thresholds.get(dimension)
        if thresholds:
            if score < thresholds[1]:
                level = 'Normal'
            elif score < thresholds[2]:
                level = 'Mild'
            elif score < thresholds[3]:
                level = 'Moderate'
            else:
                level = 'Severe'
            classifications[dimension] = level
    return classifications

# Visualization
def plot_scores(scores):
    fig, ax = plt.subplots()
    ax.bar(scores.keys(), scores.values(), color=['blue', 'orange', 'green'])
    ax.set_title('Mental Wellness Scores')
    ax.set_ylabel('Score')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

# Self-care Suggestions Placeholder
def suggest_self_care(classifications):
    suggestions = {
        'Stress': {
            'Normal': "Keep up your relaxation habits.",
            'Mild': "Try daily deep breathing or light exercise.",
            'Moderate': "Consider journaling and reducing workload.",
            'Severe': "Seek professional guidance and support groups."
        },
        'Anxiety': {
            'Normal': "Maintain mindfulness routines.",
            'Mild': "Use grounding techniques and limit caffeine.",
            'Moderate': "Practice cognitive behavioral strategies.",
            'Severe': "Consult a therapist or counselor."
        },
        'Depression': {
            'Normal': "Stay socially engaged and active.",
            'Mild': "Establish a sleep routine and stay connected.",
            'Moderate': "Include physical activity in your day.",
            'Severe': "Reach out for mental health support services."
        }
    }

    care_plan = {}
    for dim, level in classifications.items():
        care_plan[dim] = suggestions.get(dim, {}).get(level, "Try basic self-care.")
    return care_plan
