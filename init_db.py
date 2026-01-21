"""
Script d'initialisation de la base de données avec l'exemple de contact
"""
import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, SessionLocal, init_db, Contact

def init_sample_data():
    """Initialise la base de données avec l'exemple de contact"""
    
    # Créer les tables si elles n'existent pas
    init_db()
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Vérifier si des contacts existent déjà
        existing_count = db.query(Contact).count()
        if existing_count > 0:
            print(f"✅ La base de données contient déjà {existing_count} contact(s).")
            return
        
        # Données de l'exemple
        sample_contact = {
            "contactId": "550e8400-e29b-41d4-a716-446655440000",
            "nom": "Jean Dupont",
            "email": "jean.dupont@example.com",
            "entreprise": "ACME Corp",
            "poste": "Directeur Marketing",
            "evenements": [
                {
                    "date": "2025-12-10T14:30:00Z",
                    "type": "appel",
                    "notes": "Discussion sur potentiel partenariat"
                }
            ],
            "notesImportantes": [
                "Intéressé par notre solution Premium",
                "Disponible uniquement les matins"
            ],
            "prochainesActions": [
                {
                    "action": "Envoyer proposition formelle",
                    "dateEcheance": "2026-01-15"
                }
            ],
            "opportunites": [
                {
                    "projet": "Déploiement 2026",
                    "valeurEstimee": 20000
                }
            ],
            "dateCreation": "2025-11-01T09:00:00Z"
        }
        
        # Créer le contact dans la base de données
        db_contact = Contact(
            contactId=sample_contact["contactId"],
            nom=sample_contact["nom"],
            email=sample_contact["email"],
            entreprise=sample_contact["entreprise"],
            poste=sample_contact["poste"],
            evenements=json.dumps(sample_contact["evenements"], ensure_ascii=False),
            notesImportantes=json.dumps(sample_contact["notesImportantes"], ensure_ascii=False),
            prochainesActions=json.dumps(sample_contact["prochainesActions"], ensure_ascii=False),
            opportunites=json.dumps(sample_contact["opportunites"], ensure_ascii=False),
            dateCreation=datetime.fromisoformat(sample_contact["dateCreation"].replace('Z', '+00:00'))
        )
        
        db.add(db_contact)
        db.commit()
        
        print("✅ Base de données initialisée avec succès !")
        print(f"📇 Contact créé : {sample_contact['nom']} ({sample_contact['email']})")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
