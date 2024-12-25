import json
import os

SESSION_FILE = "session_history.json"

def save_session(session):
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return []
