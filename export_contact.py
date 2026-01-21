#!/usr/bin/env python3
"""
Script d'export d'un contact depuis la base SQLite vers un fichier YAML

Usage:
    python export_contact.py "Jean Dupont"
    python export_contact.py "Marie Martin" --output marie.yaml
    python export_contact.py "Jean Dupont" -o exports/jean.yaml
"""

import argparse
import sys
import yaml
from pathlib import Path
from database import SessionLocal, Contact


def export_contact_to_yaml(nom_contact, output_file=None):
    """
    Exporte un contact de la base de données vers un fichier YAML
    
    Args:
        nom_contact (str): Nom du contact à exporter
        output_file (str): Chemin du fichier de sortie (optionnel)
    
    Returns:
        bool: True si succès, False sinon
    """
    db = SessionLocal()
    
    try:
        # Rechercher le contact par nom (recherche insensible à la casse)
        contact = db.query(Contact).filter(
            Contact.nom.ilike(f"%{nom_contact}%")
        ).first()
        
        if not contact:
            print(f"❌ Aucun contact trouvé avec le nom: {nom_contact}", file=sys.stderr)
            print(f"\n💡 Astuce: Le nom peut être partiel (ex: 'Jean' pour 'Jean Dupont')", file=sys.stderr)
            return False
        
        # Convertir le contact en dictionnaire
        contact_dict = contact.to_dict()
        
        # Déterminer le nom du fichier de sortie
        if output_file is None:
            # Créer un nom de fichier basé sur le nom du contact
            safe_name = contact.nom.lower().replace(' ', '_').replace('/', '_')
            output_file = f"{safe_name}.yaml"
        
        # Créer le répertoire parent si nécessaire
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Exporter vers YAML avec une belle mise en forme
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(
                contact_dict,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                indent=2
            )
        
        print(f"✅ Contact exporté avec succès !")
        print(f"📇 Nom        : {contact.nom}")
        print(f"🏢 Entreprise : {contact.entreprise or 'N/A'}")
        print(f"📧 Email      : {contact.email or 'N/A'}")
        print(f"📄 Fichier    : {output_file}")
        
        # Afficher un aperçu du contenu
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            if len(lines) > 10:
                preview = '\n'.join(lines[:10])
                print(f"\n📋 Aperçu (10 premières lignes):")
                print("─" * 60)
                print(preview)
                print("...")
            else:
                print(f"\n📋 Contenu complet:")
                print("─" * 60)
                print(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()


def list_contacts():
    """Liste tous les contacts disponibles dans la base"""
    db = SessionLocal()
    
    try:
        contacts = db.query(Contact).order_by(Contact.nom).all()
        
        if not contacts:
            print("📇 Aucun contact dans la base de données")
            return
        
        print(f"\n📇 Liste des contacts disponibles ({len(contacts)}):")
        print("─" * 60)
        
        for contact in contacts:
            entreprise = f" ({contact.entreprise})" if contact.entreprise else ""
            email = f" - {contact.email}" if contact.email else ""
            print(f"  • {contact.nom}{entreprise}{email}")
        
        print("─" * 60)
        
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Export un contact de la base SQLite vers un fichier YAML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python export_contact.py "Jean Dupont"
  python export_contact.py "Marie" --output exports/marie.yaml
  python export_contact.py "Dupont" -o backup.yaml
  python export_contact.py --list
        """
    )
    
    parser.add_argument(
        'nom',
        nargs='?',
        help='Nom du contact à exporter (peut être partiel)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Chemin du fichier YAML de sortie (par défaut: nom_du_contact.yaml)'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='Liste tous les contacts disponibles dans la base'
    )
    
    args = parser.parse_args()
    
    # Si --list est spécifié, lister les contacts
    if args.list:
        list_contacts()
        return 0
    
    # Vérifier qu'un nom a été fourni
    if not args.nom:
        parser.print_help()
        print("\n❌ Erreur: Vous devez spécifier un nom de contact", file=sys.stderr)
        print("💡 Utilisez --list pour voir tous les contacts disponibles", file=sys.stderr)
        return 1
    
    # Exporter le contact
    success = export_contact_to_yaml(args.nom, args.output)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
