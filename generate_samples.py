
import random
from datetime import datetime, timedelta
from db import AIS, Threat, get_session, init_db

init_db()

# -----------------------------------------
# U.S. Ports (Coordinates on Land)
# -----------------------------------------

PORT_LOCATIONS = [
    ("Port of Los Angeles", 33.7361, -118.2625),
    ("Port of Houston", 29.7280, -95.2620),
    ("Port of Miami", 25.7781, -80.1794),
    ("Port of New York", 40.6681, -74.0451),
    ("Port of Charleston", 32.7816, -79.9225),
    ("Port of Corpus Christi", 27.8080, -97.3950)
]

# -----------------------------------------
# Threat Categories + Types
# -----------------------------------------

THREAT_TYPES = [
    "ransomware",
    "ais spoofing",
    "ics vulnerability",
    "navigation exploit",
    "phishing",
    "zero-day exploit",
    "credential leak"
]

THREAT_SOURCES = ["OSINT", "CISA", "DARKWEB"]


# -----------------------------------------
# Generate AIS Data
# -----------------------------------------

def generate_ais_data():
    session = get_session()

    print("Generating AIS records (land-based ports)...")

    for _ in range(80):  # Adjustable density
        port_name, lat, lon = random.choice(PORT_LOCATIONS)

        jitter_lat = lat + random.uniform(-0.01, 0.01)
        jitter_lon = lon + random.uniform(-0.01, 0.01)

        timestamp = datetime.utcnow() - timedelta(hours=random.randint(0, 72))

        # 15% AIS spoofed or anomalous
        status = random.choices(
            ["normal", "spoofed", "anomaly"],
            weights=[0.85, 0.10, 0.05]
        )[0]

        ais = AIS(
            vessel_name=port_name,
            latitude=jitter_lat,
            longitude=jitter_lon,
            timestamp=timestamp,
            status=status
        )

        session.add(ais)

    session.commit()
    session.close()

    print("Created 80 land-based AIS points.")


# -----------------------------------------
# Generate Threat Intel Data
# -----------------------------------------

def generate_threats():
    session = get_session()
    print("Generating simulated cyber threat intelligence...")

    keywords = [
        "ransomware", "zero-day", "exploit", "maritime", "OT", "ICS",
        "port systems", "GPS spoofing", "navigation", "AIS tampering"
    ]

    for _ in range(40):  # Adjustable volume
        source = random.choice(THREAT_SOURCES)
        type_ = random.choice(THREAT_TYPES)
        term = random.choice(keywords)

        summary = f"Detected {type_} threat affecting maritime systems via {source} feed."
        
        threat = Threat(
            source=source,
            type=type_,
            title=f"{source} Alert: {term} activity detected",
            link="https://example.com/intel",
            published=datetime.utcnow() - timedelta(hours=random.randint(0, 72)),
            summary=summary,
            raw="Auto-generated simulation for testing CTI pipeline"
        )

        session.add(threat)

    session.commit()
    session.close()

    print("Created 40 categorized threat intel entries.")


# -----------------------------------------
# Entrypoint
# -----------------------------------------

if __name__ == "__main__":
    generate_ais_data()
    generate_threats()





















































































