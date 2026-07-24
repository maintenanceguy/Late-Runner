import json
import os

def load_scores(filepath):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, ValueError):
        print("score file was empty or broken, starting fresh")
        return []
    except OSError as e:
        print("could not read score file:", e)
        return []


def save_score(filepath, scores):
    try:
        folder = os.path.dirname(filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(scores, f)
    except OSError as e:
        print("could not save score file:", e)


def get_high_score(scores):
    if not scores:
        return 0
    return max(scores)


def get_average_score(scores):
    if not scores:
        return 0
    return round(sum(scores) / len(scores), 1)
