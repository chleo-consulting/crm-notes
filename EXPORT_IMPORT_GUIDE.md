# Scripts d'Export/Import de Contacts 📦

Ces scripts permettent d'exporter et d'importer des contacts depuis/vers la base de données au format YAML.

## 🎯 Cas d'Usage

- **Backup manuel** d'un contact important
- **Édition avancée** d'un contact dans un éditeur de texte
- **Migration** de contacts entre environnements
- **Versioning** de contacts avec Git
- **Partage** de contacts avec l'équipe
- **Modification en masse** via scripts

## 📤 Export de Contacts

### Script : `export_contact.py`

Exporte un contact de la base SQLite vers un fichier YAML.

### Utilisation

```bash
# Lister tous les contacts disponibles
python export_contact.py --list

# Exporter un contact (par nom complet)
python export_contact.py "Jean Dupont"

# Exporter avec recherche partielle
python export_contact.py "Marie"

# Exporter vers un fichier spécifique
python export_contact.py "Jean Dupont" --output backup/jean.yaml

# Forme courte
python export_contact.py "Marie" -o exports/marie.yaml
```

### Options

| Option | Description |
|--------|-------------|
| `nom` | Nom du contact à exporter (peut être partiel) |
| `-o, --output FILE` | Chemin du fichier YAML de sortie |
| `-l, --list` | Liste tous les contacts disponibles |

### Exemples

```bash
# Export automatique (nom de fichier généré)
python export_contact.py "Jean Dupont"
# → Crée: jean_dupont.yaml

# Export avec organisation
python export_contact.py "Marie Martin" -o backups/$(date +%Y%m%d)_marie.yaml
# → Crée: backups/20260121_marie.yaml

# Export de tous les contacts
for contact in "Jean Dupont" "Marie Martin"; do
    python export_contact.py "$contact" -o "exports/${contact// /_}.yaml"
done
```

## 📥 Import/Mise à Jour de Contacts

### Script : `import_contact.py`

Import ou met à jour un contact depuis un fichier YAML.

### Utilisation

```bash
# Prévisualiser un fichier YAML
python import_contact.py contact.yaml --preview

# Tester les changements sans les appliquer (dry-run)
python import_contact.py contact.yaml --dry-run

# Mettre à jour un contact existant
python import_contact.py contact.yaml

# Créer un nouveau contact si inexistant
python import_contact.py nouveau_contact.yaml --create-if-missing
```

### Options

| Option | Description |
|--------|-------------|
| `yaml_file` | Chemin du fichier YAML à importer |
| `-c, --create-if-missing` | Créer le contact s'il n'existe pas |
| `-d, --dry-run` | Afficher les changements sans les appliquer |
| `-p, --preview` | Afficher un aperçu du fichier sans l'importer |

### Exemples

```bash
# Workflow de modification sécurisé
python export_contact.py "Jean Dupont" -o jean.yaml
# Modifier jean.yaml dans votre éditeur
python import_contact.py jean.yaml --dry-run  # Vérifier
python import_contact.py jean.yaml             # Appliquer

# Import avec création
python import_contact.py nouveau_contact.yaml --create-if-missing

# Restauration depuis backup
python import_contact.py backups/marie_20260120.yaml
```

## 📄 Format YAML

### Structure

```yaml
contactId: uuid-unique
nom: Jean Dupont
email: jean.dupont@example.com
entreprise: ACME Corp
poste: Directeur Marketing
evenements:
- date: '2025-12-10T14:30:00Z'
  type: appel
  notes: Discussion sur potentiel partenariat
notesImportantes:
- Intéressé par notre solution Premium
- Disponible uniquement les matins
prochainesActions:
- action: Envoyer proposition formelle
  dateEcheance: '2026-01-15'
opportunites:
- projet: Déploiement 2026
  valeurEstimee: 20000
dateCreation: '2025-11-01T09:00:00'
```

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `contactId` | string | **Requis**. UUID unique du contact |
| `nom` | string | Nom complet du contact |
| `email` | string | Adresse email |
| `entreprise` | string | Nom de l'entreprise |
| `poste` | string | Fonction/poste |
| `evenements` | list | Liste des événements chronologiques |
| `notesImportantes` | list | Liste de notes importantes |
| `prochainesActions` | list | Liste des actions à réaliser |
| `opportunites` | list | Liste des opportunités business |
| `dateCreation` | datetime | Date de création du contact |

## 🔄 Workflows Pratiques

### Backup Régulier

```bash
#!/bin/bash
# backup_contacts.sh - Backup automatique des contacts

DATE=$(date +%Y%m%d)
BACKUP_DIR="backups/$DATE"
mkdir -p "$BACKUP_DIR"

# Lister et exporter tous les contacts
python export_contact.py --list | grep "•" | while read -r line; do
    nom=$(echo "$line" | sed 's/.*• \([^(]*\).*/\1/' | xargs)
    filename=$(echo "$nom" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
    python export_contact.py "$nom" -o "$BACKUP_DIR/${filename}.yaml"
done

echo "✅ Backup créé dans $BACKUP_DIR"
```

### Édition Avancée

```bash
# 1. Exporter
python export_contact.py "Jean Dupont" -o jean.yaml

# 2. Éditer avec votre éditeur préféré
vim jean.yaml
# ou
code jean.yaml

# 3. Prévisualiser les changements
python import_contact.py jean.yaml --dry-run

# 4. Appliquer
python import_contact.py jean.yaml
```

### Migration entre Environnements

```bash
# Sur l'environnement source
python export_contact.py "Marie Martin" -o marie.yaml

# Copier vers l'environnement cible
scp marie.yaml user@prod:/app/imports/

# Sur l'environnement cible
python import_contact.py imports/marie.yaml --create-if-missing
```

### Versioning Git

```bash
# Exporter les contacts importants
mkdir -p contacts_vcs
python export_contact.py "Jean Dupont" -o contacts_vcs/jean.yaml
python export_contact.py "Marie Martin" -o contacts_vcs/marie.yaml

# Versionner
git add contacts_vcs/
git commit -m "feat: Ajouter contacts VIP"

# Restaurer depuis l'historique
git show HEAD~1:contacts_vcs/jean.yaml > jean_old.yaml
python import_contact.py jean_old.yaml
```

## ⚠️ Remarques Importantes

### Sécurité
- Les fichiers YAML contiennent des données sensibles
- Ne les commitez pas dans des repos publics
- Ajoutez `*.yaml` au `.gitignore` si nécessaire
- Chiffrez les backups contenant des informations confidentielles

### ID de Contact
- Le `contactId` est essentiel pour identifier le contact
- Ne modifiez jamais le `contactId` dans le YAML
- Pour créer un nouveau contact, générez un nouvel UUID

### Encodage
- Les fichiers YAML sont encodés en UTF-8
- Les caractères spéciaux et accents sont supportés
- Les dates sont au format ISO 8601

### Performance
- L'export est instantané même pour des contacts complexes
- L'import valide la structure avant d'appliquer les changements
- Utilisez `--dry-run` pour valider sans risque

## 🐛 Dépannage

### "Contact non trouvé"
```bash
# Lister tous les contacts
python export_contact.py --list

# Essayer avec un nom partiel
python export_contact.py "Jean"  # au lieu de "Jean Dupont"
```

### "Format YAML invalide"
```bash
# Vérifier la syntaxe YAML
python -c "import yaml; yaml.safe_load(open('contact.yaml'))"

# Prévisualiser avant import
python import_contact.py contact.yaml --preview
```

### "Contact avec ID XXX non trouvé"
```bash
# Utiliser --create-if-missing pour créer
python import_contact.py contact.yaml --create-if-missing
```

## 📚 Ressources

- Documentation YAML: https://yaml.org/
- Format des dates ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
- Python PyYAML: https://pyyaml.org/

## 💡 Astuces

### Recherche Partielle
Le script d'export accepte des noms partiels :
```bash
python export_contact.py "Jean"     # Trouve "Jean Dupont"
python export_contact.py "Martin"   # Trouve "Marie Martin"
python export_contact.py "ACME"     # Non supporté (nom uniquement)
```

### Édition Rapide
```bash
# Éditer directement puis réimporter
python export_contact.py "Jean" -o /tmp/jean.yaml && \
vim /tmp/jean.yaml && \
python import_contact.py /tmp/jean.yaml
```

### Validation Avant Commit
```bash
# Hook pre-commit pour valider les YAMLs
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
for file in $(git diff --cached --name-only | grep '\.yaml$'); do
    python import_contact.py "$file" --dry-run || exit 1
done
EOF
chmod +x .git/hooks/pre-commit
```

---

**Créé avec ❤️ pour faciliter la gestion de vos contacts business**
