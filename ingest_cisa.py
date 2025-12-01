import feedparser
from datetime import datetime
from db import Threat, init_db, get_session

CISA_FEED = "https://www.cisa.gov/cybersecurity-advisories/all.xml"

def ingest_cisa():
    print("Fetching CISA advisory feed...")
    feed = feedparser.parse(CISA_FEED)

    session = get_session()
    count = 0

    for entry in feed.entries:
        exists = session.query(Threat).filter_by(title=entry.title).first()
        if exists:
            continue

        threat = Threat(
            source="CISA",
            title=entry.title,
            link=entry.link,
            published=datetime(*entry.published_parsed[:6]),
            summary=entry.summary,
            raw=str(entry)
        )

        session.add(threat)
        count += 1

    session.commit()
    session.close()

    print(f"Ingested {count} new CISA advisories.")

if __name__ == "__main__":
    init_db()
    ingest_cisa()

