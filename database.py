"""
SQLite database management module for contact records
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# SQLite database configuration
DATABASE_URL = "sqlite:///./data/contacts.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Contact(Base):
    """Contact table model with JSON columns for structured data"""
    __tablename__ = "contacts"

    contactId = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    company = Column(String, index=True)
    position = Column(String)
    events = Column(Text)  # Stored as JSON
    importantNotes = Column(Text)  # Stored as JSON
    nextActions = Column(Text)  # Stored as JSON
    opportunities = Column(Text)  # Stored as JSON
    createdAt = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert Contact object to JSON dictionary"""
        return {
            "contactId": self.contactId,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "position": self.position,
            "events": json.loads(self.events) if self.events else [],
            "importantNotes": json.loads(self.importantNotes) if self.importantNotes else [],
            "nextActions": json.loads(self.nextActions) if self.nextActions else [],
            "opportunities": json.loads(self.opportunities) if self.opportunities else [],
            "createdAt": self.createdAt.isoformat() if self.createdAt else None
        }


def get_db():
    """Database session generator for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database (create tables)"""
    Base.metadata.create_all(bind=engine)
