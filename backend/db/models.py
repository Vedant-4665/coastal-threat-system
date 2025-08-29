from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    pressure = Column(Float)
    description = Column(String)
    source = Column(String, default="openweather")

class TideData(Base):
    __tablename__ = "tide_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String, index=True)
    tide_height = Column(Float)
    tide_type = Column(String)  # high, low, rising, falling
    source = Column(String, default="noaa")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_type = Column(String, index=True)  # cyclone, high_tide, storm_surge
    severity = Column(String, index=True)    # low, medium, high, critical
    location = Column(String, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    triggered_by = Column(String)  # rule_based, ml_anomaly, forecast
    data_sources = Column(String)  # weather, tide, pressure, etc.
    source = Column(String, default="system")  # system, api, manual

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./coastal_threats.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
