#!/usr/bin/env python3
"""
Script d'import/mise à jour d'un contact depuis un fichier YAML vers la base SQLite

Usage:
    python import_contact.py contact.yaml
    python import_contact.py marie.yaml --create-if-missing
    python import_contact.py jean.yaml --dry-run
"""

import argparse
import sys
import yaml
import json
from pathlib import Path
from database import SessionLocal, Contact


def import_contact_from_yaml(yaml_file, create_if_missing=False, dry_run=False):
    """
    Import ou met à jour un contact depuis un fichier YAML
    
    Args:
        yaml_file (str): Chemin du fichier YAML à importer
        create_if_missing (bool): Créer le contact s'il n'existe pas
        dry_run (bool): Afficher les changements sans les appliquer
    
    Returns:
        bool: True si succès, False sinon
    """
    # Vérifier que le fichier existe
    yaml_path = Path(yaml_file)
    if not yaml_path.exists():
        print(f"❌ Fichier non trouvé: {yaml_file}", file=sys.stderr)
        return False
    
    # Charger le fichier YAML
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            contact_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ Erreur lors de la lecture du fichier YAML: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}", file=sys.stderr)
        return False
    
    # Vérifier que les données sont valides
    if not isinstance(contact_data, dict):
        print(f"❌ Format YAML invalide: le fichier doit contenir un dictionnaire", file=sys.stderr)
        return False
    
    if 'contactId' not in contact_data:
        print(f"❌ Le fichier YAML doit contenir un champ 'contactId'", file=sys.stderr)
        return False
    
    db = SessionLocal()
    
    try:
        # Rechercher le contact existant par ID
        contact_id = contact_data['contactId']
        existing_contact = db.query(Contact).filter(Contact.contactId == contact_id).first()
        
        if existing_contact:
            print(f"📇 Contact trouvé: {existing_contact.nom}")
            print(f"🔄 Mode: Mise à jour")
            action = "mise à jour"
            contact = existing_contact
        else:
            if not create_if_missing:
                print(f"❌ Contact avec ID {contact_id} non trouvé", file=sys.stderr)
                print(f"💡 Utilisez --create-if-missing pour créer un nouveau contact", file=sys.stderr)
                return False
            
            print(f"➕ Contact non trouvé, création d'un nouveau contact")
            print(f"🆕 Mode: Création")
            action = "création"
            contact = Contact(contactId=contact_id)
            db.add(contact)
        
        # Afficher les changements
        print(f"\n📊 Changements à appliquer:")
        print("─" * 60)
        
        changes = []
        
        # Mettre à jour les champs simples
        for field in ['nom', 'email', 'entreprise', 'poste']:
            if field in contact_data:
                old_value = getattr(contact, field, None)
                new_value = contact_data[field]
                
                if old_value != new_value:
                    print(f"  {field:20} : {old_value or '(vide)'} → {new_value or '(vide)'}")
                    changes.append(field)
                    
                    if not dry_run:
                        setattr(contact, field, new_value)
        
        # Mettre à jour les champs JSON (listes)
        for field in ['evenements', 'notesImportantes', 'prochainesActions', 'opportunites']:
            if field in contact_data:
                new_value = contact_data[field]
                
                # Comparer avec l'ancienne valeur
                if existing_contact:
                    old_json = getattr(existing_contact, field, None)
                    if old_json:
                        old_value = json.loads(old_json)
                    else:
                        old_value = []
                else:
                    old_value = []
                
                if old_value != new_value:
                    print(f"  {field:20} : {len(old_value)} élément(s) → {len(new_value)} élément(s)")
                    changes.append(field)
                    
                    if not dry_run:
                        setattr(contact, field, json.dumps(new_value, ensure_ascii=False))
        
        if not changes:
            print("  ℹ️  Aucun changement détecté")
            return True
        
        print("─" * 60)
        print(f"\n📈 Nombre de champs modifiés: {len(changes)}")
        
        if dry_run:
            print(f"\n🔍 Mode DRY-RUN: Aucune modification appliquée")
            print(f"💡 Retirez --dry-run pour appliquer les changements")
            return True
        
        # Appliquer les changements
        db.commit()
        db.refresh(contact)
        
        print(f"\n✅ {action.capitalize()} réussie !")
        print(f"📇 Contact   : {contact.nom}")
        print(f"🆔 ID        : {contact.contactId}")
        print(f"🏢 Entreprise: {contact.entreprise or 'N/A'}")
        print(f"📧 Email     : {contact.email or 'N/A'}")
        
        # Afficher un résumé des données
        contact_dict = contact.to_dict()
        print(f"\n📊 Résumé:")
        print(f"  • Événements       : {len(contact_dict.get('evenements', []))}")
        print(f"  • Notes importantes: {len(contact_dict.get('notesImportantes', []))}")
        print(f"  • Prochaines actions: {len(contact_dict.get('prochainesActions', []))}")
        print(f"  • Opportunités     : {len(contact_dict.get('opportunites', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    
    finally:
        db.close()


def preview_yaml_file(yaml_file):
    """Affiche un aperçu du fichier YAML"""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            contact_data = yaml.safe_load(f)
        
        print(f"\n📄 Aperçu du fichier: {yaml_file}")
        print("─" * 60)
        
        if 'nom' in contact_data:
            print(f"📇 Nom        : {contact_data['nom']}")
        if 'email' in contact_data:
            print(f"📧 Email      : {contact_data['email']}")
        if 'entreprise' in contact_data:
            print(f"🏢 Entreprise : {contact_data['entreprise']}")
        if 'poste' in contact_data:
            print(f"💼 Poste      : {contact_data['poste']}")
        if 'contactId' in contact_data:
            print(f"🆔 ID         : {contact_data['contactId']}")
        
        print(f"\n📊 Données structurées:")
        for field in ['evenements', 'notesImportantes', 'prochainesActions', 'opportunites']:
            if field in contact_data and isinstance(contact_data[field], list):
                print(f"  • {field:20} : {len(contact_data[field])} élément(s)")
        
        print("─" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Import ou met à jour un contact depuis un fichier YAML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python import_contact.py contact.yaml
  python import_contact.py marie.yaml --create-if-missing
  python import_contact.py jean.yaml --dry-run
  python import_contact.py contact.yaml --preview
        """
    )
    
    parser.add_argument(
        'yaml_file',
        help='Chemin du fichier YAML à importer'
    )
    
    parser.add_argument(
        '-c', '--create-if-missing',
        action='store_true',
        help='Créer le contact s\'il n\'existe pas dans la base'
    )
    
    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Afficher les changements sans les appliquer'
    )
    
    parser.add_argument(
        '-p', '--preview',
        action='store_true',
        help='Afficher un aperçu du fichier YAML sans l\'importer'
    )
    
    args = parser.parse_args()
    
    # Si --preview est spécifié, afficher l'aperçu seulement
    if args.preview:
        success = preview_yaml_file(args.yaml_file)
        return 0 if success else 1
    
    # Importer le contact
    success = import_contact_from_yaml(
        args.yaml_file,
        create_if_missing=args.create_if_missing,
        dry_run=args.dry_run
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
