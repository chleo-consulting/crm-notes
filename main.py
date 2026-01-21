"""
Application FastAPI pour la gestion des fiches de contact
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

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Gestionnaire de Contacts Business",
    description="API pour gérer vos fiches de contacts professionnels",
    version="1.0.0"
)

# Montage des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialisation de la base de données au démarrage
@app.on_event("startup")
def startup_event():
    init_db()


# ============= ROUTES WEB =============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil avec l'interface utilisateur"""
    return templates.TemplateResponse("index.html", {"request": request})


# ============= API ENDPOINTS =============

@app.post("/api/contacts", response_model=ContactResponse, status_code=201)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle fiche de contact"""
    
    # Génération d'un UUID unique pour le contact
    contact_id = str(uuid.uuid4())
    
    # Création de l'objet Contact pour SQLAlchemy
    db_contact = Contact(
        contactId=contact_id,
        nom=contact.nom,
        email=contact.email,
        entreprise=contact.entreprise,
        poste=contact.poste,
        evenements=json.dumps([e.dict() for e in contact.evenements], ensure_ascii=False),
        notesImportantes=json.dumps(contact.notesImportantes, ensure_ascii=False),
        prochainesActions=json.dumps([a.dict() for a in contact.prochainesActions], ensure_ascii=False),
        opportunites=json.dumps([o.dict() for o in contact.opportunites], ensure_ascii=False)
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
    """Récupérer la liste de tous les contacts avec recherche optionnelle"""
    
    query = db.query(Contact)
    
    # Filtrage par recherche si fournie
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Contact.nom.like(search_filter)) |
            (Contact.email.like(search_filter)) |
            (Contact.entreprise.like(search_filter)) |
            (Contact.poste.like(search_filter))
        )
    
    contacts = query.order_by(Contact.dateCreation.desc()).all()
    return [contact.to_dict() for contact in contacts]


@app.get("/api/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: str, db: Session = Depends(get_db)):
    """Récupérer une fiche de contact spécifique par ID"""
    
    contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    
    return contact.to_dict()


@app.put("/api/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une fiche de contact existante"""
    
    contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    
    # Mise à jour des champs fournis
    update_data = contact_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in ['evenements', 'prochainesActions', 'opportunites']:
            # Conversion des listes d'objets en JSON
            setattr(contact, field, json.dumps([item.dict() for item in value], ensure_ascii=False))
        elif field == 'notesImportantes':
            setattr(contact, field, json.dumps(value, ensure_ascii=False))
        else:
            setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    
    return contact.to_dict()


@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: str, db: Session = Depends(get_db)):
    """Supprimer une fiche de contact"""
    
    contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact non trouvé")
    
    db.delete(contact)
    db.commit()
    
    return {"message": "Contact supprimé avec succès", "contactId": contact_id}


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir des statistiques sur les contacts"""
    
    total_contacts = db.query(Contact).count()
    
    contacts = db.query(Contact).all()
    total_opportunites = 0
    valeur_totale = 0.0
    
    for contact in contacts:
        if contact.opportunites:
            opps = json.loads(contact.opportunites)
            total_opportunites += len(opps)
            for opp in opps:
                if 'valeurEstimee' in opp and opp['valeurEstimee']:
                    valeur_totale += float(opp['valeurEstimee'])
    
    return {
        "totalContacts": total_contacts,
        "totalOpportunites": total_opportunites,
        "valeurTotaleOpportunites": valeur_totale
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
