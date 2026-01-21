"""
Modèles Pydantic pour la validation des données
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class Evenement(BaseModel):
    """Modèle pour un événement dans la chronologie"""
    date: str
    type: str
    notes: str


class ProchaineAction(BaseModel):
    """Modèle pour une prochaine action"""
    action: str
    dateEcheance: str


class Opportunite(BaseModel):
    """Modèle pour une opportunité business"""
    projet: str
    valeurEstimee: Optional[float] = None


class ContactBase(BaseModel):
    """Modèle de base pour un contact"""
    nom: str
    email: Optional[str] = None
    entreprise: Optional[str] = None
    poste: Optional[str] = None
    evenements: List[Evenement] = []
    notesImportantes: List[str] = []
    prochainesActions: List[ProchaineAction] = []
    opportunites: List[Opportunite] = []


class ContactCreate(ContactBase):
    """Modèle pour créer un contact (sans ID)"""
    pass


class ContactUpdate(BaseModel):
    """Modèle pour mettre à jour un contact (tous les champs optionnels)"""
    nom: Optional[str] = None
    email: Optional[str] = None
    entreprise: Optional[str] = None
    poste: Optional[str] = None
    evenements: Optional[List[Evenement]] = None
    notesImportantes: Optional[List[str]] = None
    prochainesActions: Optional[List[ProchaineAction]] = None
    opportunites: Optional[List[Opportunite]] = None


class ContactResponse(ContactBase):
    """Modèle de réponse pour un contact (avec ID et date)"""
    contactId: str
    dateCreation: str

    class Config:
        from_attributes = True
