"""
Pydantic models for data validation
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class Event(BaseModel):
    """Model for an event in the timeline"""
    date: str
    type: str
    notes: str


class NextAction(BaseModel):
    """Model for a next action"""
    action: str
    dueDate: str


class Opportunity(BaseModel):
    """Model for a business opportunity"""
    project: str
    estimatedValue: Optional[float] = None


class ContactBase(BaseModel):
    """Base model for a contact"""
    name: str
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    events: List[Event] = []
    importantNotes: List[str] = []
    nextActions: List[NextAction] = []
    opportunities: List[Opportunity] = []


class ContactCreate(ContactBase):
    """Model for creating a contact (without ID)"""
    pass


class ContactUpdate(BaseModel):
    """Model for updating a contact (all fields optional)"""
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    events: Optional[List[Event]] = None
    importantNotes: Optional[List[str]] = None
    nextActions: Optional[List[NextAction]] = None
    opportunities: Optional[List[Opportunity]] = None


class ContactResponse(ContactBase):
    """Response model for a contact (with ID and date)"""
    contactId: str
    createdAt: str

    class Config:
        from_attributes = True
