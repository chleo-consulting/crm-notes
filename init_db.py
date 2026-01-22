"""
Database initialization script with sample contact
"""
import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, SessionLocal, init_db, Contact

def init_sample_data():
    """Initialize database with sample contact"""
    
    # Create tables if they don't exist
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if contacts already exist
        existing_count = db.query(Contact).count()
        if existing_count > 0:
            print(f"✅ Database already contains {existing_count} contact(s).")
            return
        
        # Sample data
        sample_contact = {
            "contactId": "550e8400-e29b-41d4-a716-446655440000",
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "ACME Corp",
            "position": "Marketing Director",
            "events": [
                {
                    "date": "2025-12-10T14:30:00Z",
                    "type": "call",
                    "notes": "Discussion about potential partnership"
                }
            ],
            "importantNotes": [
                "Interested in our Premium solution",
                "Available only in the mornings"
            ],
            "nextActions": [
                {
                    "action": "Send formal proposal",
                    "dueDate": "2026-01-15"
                }
            ],
            "opportunities": [
                {
                    "project": "2026 Deployment",
                    "estimatedValue": 20000
                }
            ],
            "createdAt": "2025-11-01T09:00:00Z"
        }
        
        # Create contact in database
        db_contact = Contact(
            contactId=sample_contact["contactId"],
            name=sample_contact["name"],
            email=sample_contact["email"],
            company=sample_contact["company"],
            position=sample_contact["position"],
            events=json.dumps(sample_contact["events"], ensure_ascii=False),
            importantNotes=json.dumps(sample_contact["importantNotes"], ensure_ascii=False),
            nextActions=json.dumps(sample_contact["nextActions"], ensure_ascii=False),
            opportunities=json.dumps(sample_contact["opportunities"], ensure_ascii=False),
            createdAt=datetime.fromisoformat(sample_contact["createdAt"].replace('Z', '+00:00'))
        )
        
        db.add(db_contact)
        db.commit()
        
        print("✅ Database initialized successfully!")
        print(f"📇 Contact created: {sample_contact['name']} ({sample_contact['email']})")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
