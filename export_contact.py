#!/usr/bin/env python3
"""
Script d'export d'un contact depuis la base SQLite vers un fichier YAML

Usage:
    python export_contact.py "Jean Dupont"
    python export_contact.py "Marie Martin" --output marie.yaml
    python export_contact.py "Jean Dupont" -o exports/jean.yaml
    python export_contact.py --all
    python export_contact.py --all --output exports/
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
        # Search for contact by name (case-insensitive)
        contact = db.query(Contact).filter(
            Contact.name.ilike(f"%{nom_contact}%")
        ).first()
        
        if not contact:
            print(f"❌ Aucun contact trouvé avec le nom: {nom_contact}", file=sys.stderr)
            print(f"\n💡 Astuce: Le nom peut être partiel (ex: 'Jean' pour 'Jean Dupont')", file=sys.stderr)
            return False
        
        # Convertir le contact en dictionnaire
        contact_dict = contact.to_dict()
        
        # Déterminer le nom du fichier de sortie
        if output_file is None:
            # Create filename based on contact name
            safe_name = contact.name.lower().replace(' ', '_').replace('/', '_')
            output_file = f"data/contacts/{safe_name}.yaml"
        
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
        
        print(f"✅ Contact exported successfully!")
        print(f"📇 Name       : {contact.name}")
        print(f"🏢 Company    : {contact.company or 'N/A'}")
        print(f"📧 Email      : {contact.email or 'N/A'}")
        print(f"📞 Phone      : {contact.phone or 'N/A'}")
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


def export_all_contacts(output_dir=None):
    """
    Exporte tous les contacts de la base de données vers des fichiers YAML
    
    Args:
        output_dir (str): Répertoire de sortie (par défaut: data/contacts/)
    
    Returns:
        tuple: (nombre de succès, nombre d'échecs)
    """
    db = SessionLocal()
    
    # Définir le répertoire de sortie par défaut
    if output_dir is None:
        output_dir = "data/contacts/"
    
    # S'assurer que le chemin se termine par /
    output_dir = output_dir.rstrip('/') + '/'
    
    try:
        # Récupérer tous les contacts
        contacts = db.query(Contact).order_by(Contact.name).all()
        
        if not contacts:
            print("📇 Aucun contact dans la base de données")
            return 0, 0
        
        print(f"\n🚀 Export de {len(contacts)} contact(s)...")
        print(f"📁 Répertoire de sortie: {output_dir}")
        print("─" * 60)
        
        success_count = 0
        error_count = 0
        
        # Créer le répertoire de sortie
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Exporter chaque contact
        for i, contact in enumerate(contacts, 1):
            try:
                # Créer un nom de fichier sûr
                safe_name = contact.name.lower().replace(' ', '_').replace('/', '_')
                output_file = f"{output_dir}{safe_name}.yaml"
                
                # Convertir le contact en dictionnaire
                contact_dict = contact.to_dict()
                
                # Exporter vers YAML
                with open(output_file, 'w', encoding='utf-8') as f:
                    yaml.dump(
                        contact_dict,
                        f,
                        allow_unicode=True,
                        default_flow_style=False,
                        sort_keys=False,
                        indent=2
                    )
                
                company = f" ({contact.company})" if contact.company else ""
                print(f"  [{i}/{len(contacts)}] ✅ {contact.name}{company} → {output_file}")
                success_count += 1
                
            except Exception as e:
                print(f"  [{i}/{len(contacts)}] ❌ {contact.name} - Erreur: {e}")
                error_count += 1
        
        print("─" * 60)
        print(f"\n📊 Résumé:")
        print(f"  ✅ Succès: {success_count}")
        print(f"  ❌ Échecs: {error_count}")
        print(f"  📁 Fichiers créés dans: {output_dir}")
        
        return success_count, error_count
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export global: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 0, 0
    
    finally:
        db.close()


def list_contacts():
    """List all available contacts in the database"""
    db = SessionLocal()
    
    try:
        contacts = db.query(Contact).order_by(Contact.name).all()
        
        if not contacts:
            print("📇 Aucun contact dans la base de données")
            return
        
        print(f"\n📇 Liste des contacts disponibles ({len(contacts)}):")
        print("─" * 60)
        
        for contact in contacts:
            company = f" ({contact.company})" if contact.company else ""
            email = f" - {contact.email}" if contact.email else ""
            print(f"  • {contact.name}{company}{email}")
        
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
  python export_contact.py --all
  python export_contact.py --all --output exports/
        """
    )
    
    parser.add_argument(
        'nom',
        nargs='?',
        help='Nom du contact à exporter (peut être partiel)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Chemin du fichier YAML de sortie (par défaut: data/contacts/nom_du_contact.yaml) ou répertoire pour --all'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='Liste tous les contacts disponibles dans la base'
    )
    
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Exporte tous les contacts (répertoire par défaut: data/contacts/)'
    )
    
    args = parser.parse_args()
    
    # Si --list est spécifié, lister les contacts
    if args.list:
        list_contacts()
        return 0
    
    # Si --all est spécifié, exporter tous les contacts
    if args.all:
        success, errors = export_all_contacts(args.output)
        return 0 if errors == 0 else 1
    
    # Vérifier qu'un nom a été fourni
    if not args.nom:
        parser.print_help()
        print("\n❌ Erreur: Vous devez spécifier un nom de contact ou utiliser --all", file=sys.stderr)
        print("💡 Utilisez --list pour voir tous les contacts disponibles", file=sys.stderr)
        return 1
    
    # Exporter le contact
    success = export_contact_to_yaml(args.nom, args.output)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
