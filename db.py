from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///threats.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True)
    source = Column(String)    
    type = Column(String)      
    title = Column(String)
    link = Column(String)
    published = Column(DateTime)
    summary = Column(String)
    raw = Column(String)

class AIS(Base):
    __tablename__ = "ais"

    id = Column(Integer, primary_key=True)
    vessel_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    status = Column(String)     


def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
