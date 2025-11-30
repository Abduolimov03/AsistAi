import json
import os

HISTORY_FILE = "history.json"

def save_history(user_id: int, question: str, answer: str):
    data = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    if str(user_id) not in data:
        data[str(user_id)] = []

    data[str(user_id)].append({"question": question, "answer": answer})

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clear_history(user_id: int):
    if not os.path.exists(HISTORY_FILE):
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.pop(str(user_id), None)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
