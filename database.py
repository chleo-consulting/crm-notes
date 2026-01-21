"""
Module de gestion de la base de données SQLite pour les fiches de contact
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# Configuration de la base de données SQLite
DATABASE_URL = "sqlite:///./contacts.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Contact(Base):
    """Modèle de la table contacts avec colonnes JSON pour les données structurées"""
    __tablename__ = "contacts"

    contactId = Column(String, primary_key=True, index=True)
    nom = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    entreprise = Column(String, index=True)
    poste = Column(String)
    evenements = Column(Text)  # Stocké en JSON
    notesImportantes = Column(Text)  # Stocké en JSON
    prochainesActions = Column(Text)  # Stocké en JSON
    opportunites = Column(Text)  # Stocké en JSON
    dateCreation = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convertit l'objet Contact en dictionnaire JSON"""
        return {
            "contactId": self.contactId,
            "nom": self.nom,
            "email": self.email,
            "entreprise": self.entreprise,
            "poste": self.poste,
            "evenements": json.loads(self.evenements) if self.evenements else [],
            "notesImportantes": json.loads(self.notesImportantes) if self.notesImportantes else [],
            "prochainesActions": json.loads(self.prochainesActions) if self.prochainesActions else [],
            "opportunites": json.loads(self.opportunites) if self.opportunites else [],
            "dateCreation": self.dateCreation.isoformat() if self.dateCreation else None
        }


def get_db():
    """Générateur de session de base de données pour FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialise la base de données (crée les tables)"""
    Base.metadata.create_all(bind=engine)
