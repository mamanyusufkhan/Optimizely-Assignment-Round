_TEMPS = {
    "paris": "18",
    "london": 17.0,
    "dhaka": 31,
    "amsterdam": "19.5"
}

def temp(city: str):
    c = (city or "").strip()
    return _TEMPS.get(c, "20")
