from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# -----------------------------
# Database Setup
# -----------------------------

DATABASE_URL = "sqlite:///threats.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite + Streamlit
    echo=False
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# -----------------------------
# Threat Table
# -----------------------------

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True)
    source = Column(String)     # OSINT, CISA, DARKWEB
    type = Column(String)       # ransomware, spoofing, ICS vuln, phishing, etc.
    title = Column(String)
    link = Column(String)
    published = Column(DateTime)
    summary = Column(String)
    raw = Column(String)


# -----------------------------
# AIS Table
# -----------------------------

class AIS(Base):
    __tablename__ = "ais"

    id = Column(Integer, primary_key=True)
    vessel_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    status = Column(String)     # normal, spoofed, anomaly


# -----------------------------
# Helper: Create DB / Tables
# -----------------------------

def init_db():
    Base.metadata.create_all(bind=engine)


# -----------------------------
# Helper: Get Session
# -----------------------------

def get_session():
    return SessionLocal()
