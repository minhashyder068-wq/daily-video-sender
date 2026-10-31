import re

BASE = ["#DailyVlog", "#DailyDiary", "#Shorts", "#ViralShorts", "#AIVideo"]

def make_hashtags(text, limit=12):
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    stop = {"the","and","for","with","this","that","from","have","was","were","today","into","about"}
    tags = []
    for w in words:
        if len(w) >= 4 and w not in stop:
            tag = "#" + w.capitalize()
            if tag not in tags:
                tags.append(tag)
    return (tags + BASE)[:limit]
