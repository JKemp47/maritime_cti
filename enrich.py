import json
from datetime import datetime
from db import Threat, get_session

KEYWORDS = [
    "gps", "spoof", "ais", "navigation",
    "malware", "ransomware", "phishing",
    "exploit", "zero-day"
]

with open("mitre_mapping.json") as f:
    MITRE_MAP = json.load(f)

def enrich():
    session = get_session()
    threats = session.query(Threat).all()
    updated = 0

    for t in threats:
        text = (t.title + " " + t.summary).lower()

        found_keywords = [k for k in KEYWORDS if k in text]
        t.keywords = ",".join(found_keywords)

        # scoring system
        score = 0
        if "ransomware" in text:
            score = 90
        elif "spoof" in text:
            score = 75
        elif "phishing" in text:
            score = 60
        elif "exploit" in text:
            score = 70

        t.score = score

        mitre_ids = []
        for k in found_keywords:
            if k in MITRE_MAP:
                mitre_ids.append(MITRE_MAP[k])

        t.mitre = ",".join(mitre_ids)
        updated += 1

    session.commit()
    session.close()

    print(f"Enriched {updated} threat items at {datetime.utcnow()}.")

if __name__ == "__main__":
    enrich()

