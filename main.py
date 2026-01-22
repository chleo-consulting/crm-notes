"""
FastAPI application for contact management
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import json
import uuid

from database import get_db, init_db, Contact
from models import ContactCreate, ContactUpdate, ContactResponse

# Initialize FastAPI application
app = FastAPI(
    title="Business Contact Manager",
    description="API to manage your professional contact records",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


# ============= WEB ROUTES =============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with user interface"""
    return templates.TemplateResponse("index.html", {"request": request})


# ============= API ENDPOINTS =============

@app.post("/api/contacts", response_model=ContactResponse, status_code=201)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Create a new contact record"""
    
    # Generate unique UUID for the contact
    contact_id = str(uuid.uuid4())
    
    # Create Contact object for SQLAlchemy
    db_contact = Contact(
        contactId=contact_id,
        name=contact.name,
        email=contact.email,
        company=contact.company,
        position=contact.position,
        events=json.dumps([e.model_dump() for e in contact.events], ensure_ascii=False),
        importantNotes=json.dumps(contact.importantNotes, ensure_ascii=False),
        nextActions=json.dumps([a.model_dump() for a in contact.nextActions], ensure_ascii=False),
        opportunities=json.dumps([o.model_dump() for o in contact.opportunities], ensure_ascii=False)
    )
    
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    return db_contact.to_dict()


@app.get("/api/contacts", response_model=List[ContactResponse])
async def get_contacts(
    search: str = None,
    db: Session = Depends(get_db)
):
    """Get list of all contacts with optional search"""
    
    query = db.query(Contact)
    
    # Filter by search if provided
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Contact.name.like(search_filter)) |
            (Contact.email.like(search_filter)) |
            (Contact.company.like(search_filter)) |
            (Contact.position.like(search_filter))
        )
    
    contacts = query.order_by(Contact.createdAt.desc()).all()
    return [contact.to_dict() for contact in contacts]


@app.get("/api/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: str, db: Session = Depends(get_db)):
    """Get a specific contact record by ID"""
    
    contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contact.to_dict()


@app.put("/api/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing contact record"""
    
    contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # Update provided fields
    update_data = contact_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in ['events', 'nextActions', 'opportunities']:
            # model_dump() already returns dictionaries
            setattr(contact, field, json.dumps(value, ensure_ascii=False))
        elif field == 'importantNotes':
            setattr(contact, field, json.dumps(value, ensure_ascii=False))
        else:
            setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    
    return contact.to_dict()


@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: str, db: Session = Depends(get_db)):
    """Delete a contact record"""
    
    contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    
    return {"message": "Contact deleted successfully", "contactId": contact_id}


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about contacts"""
    
    total_contacts = db.query(Contact).count()
    
    contacts = db.query(Contact).all()
    total_opportunities = 0
    total_value = 0.0
    
    for contact in contacts:
        if contact.opportunities:
            opps = json.loads(contact.opportunities)
            total_opportunities += len(opps)
            for opp in opps:
                if 'estimatedValue' in opp and opp['estimatedValue']:
                    total_value += float(opp['estimatedValue'])
    
    return {
        "totalContacts": total_contacts,
        "totalOpportunities": total_opportunities,
        "totalOpportunitiesValue": total_value
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
