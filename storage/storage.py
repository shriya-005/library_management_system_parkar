import json
from pathlib import Path
FILE = Path(__file__).parent.parent / "data" /"library.json"
def load_data():
    if not FILE.exists():
        return {"books": [],"members": []}
    with open(FILE, "r", encoding="utf-8")as f:
        return json.load(f)
def save_data(books,members):
    FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE, "w", encoding="utf-8")as f:
        json.dump({"books": books,"members": members}, f, indent=4) 