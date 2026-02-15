from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./incidents.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    direction = Column(String)  # INBOUND (User -> LLM) or OUTBOUND (LLM -> User)
    source_ip = Column(String, nullable=True)
    input_text = Column(String)
    risk_score = Column(Float)
    risk_level = Column(String)  # LOW, MEDIUM, HIGH, CRITICAL
    detected_threats = Column(JSON)  # List of threats found
    action_taken = Column(String)  # ALLOW, BLOCK, QUARANTINE, ESCALATE
    extra_info = Column(JSON, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
