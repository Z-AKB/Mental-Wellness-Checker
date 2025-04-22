# -*- coding: utf-8 -*-
def calculate_score(answers, question_keys):
    """
    Calculate the total score from the selected answers.
    Each answer is expected to be an integer value.
    :param answers: a dict-like object (e.g., request.form) containing answers.
    :param question_keys: a list of keys (e.g., ['question1', 'question2'])
    :return: integer score
    """
    try:
        score = sum(int(answers.get(key, 0)) for key in question_keys)
    except ValueError:
        score = 0
    return score


def classify_wellness(score):
    """
    Classify wellness based on score thresholds.
    This function assigns a classification based on the total score.
    Thresholds are examples and should be refined based on the clinical scale.

    :param score: total integer score
    :return: classification string
    """
    if score <= 5:
        return "Excellent"
    elif 6 <= score <= 10:
        return "Good"
    elif 11 <= score <= 15:
        return "Fair"
    else:
        return "Poor"


def get_self_care_routines(classification):
    """
    Return a list of self-care suggestions based on the user's wellness classification.

    :param classification: wellness level as string
    :return: list of suggestions
    """
    routines = {
        "Excellent": [
            "Keep doing what you're doing!",
            "Maintain a consistent sleep schedule.",
            "Engage in activities that bring you joy."
        ],
        "Good": [
            "Take short breaks during the day.",
            "Practice mindfulness or meditation.",
            "Stay socially connected."
        ],
        "Fair": [
            "Consider talking to a mental health professional.",
            "Limit screen time before bed.",
            "Practice gratitude journaling."
        ],
        "Poor": [
            "Seek support from a licensed therapist or counselor.",
            "Talk to someone you trust.",
            "Avoid isolation and try to engage in small, calming activities."
        ]
    }
    return routines.get(classification, ["Stay safe and take care."])
