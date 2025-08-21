import json

def kb_lookup(q: str) -> str:
    try:
        with open("data/kb.json","r") as f:
            data = json.load(f)
        for item in data.get("entries", []):
            if q in item.get("name",""):
                return item.get("summary","")
        return "No entry found."
    except Exception as e:
        return f"KB error: {e}"
