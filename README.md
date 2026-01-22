# Gestionnaire de Contacts Business 📇

Application web complète de gestion de contacts professionnels avec FastAPI, SQLite et interface utilisateur moderne.

## 🎯 Fonctionnalités

- **CRUD complet** : Créer, Lire, Modifier, Supprimer des fiches de contact
- **Recherche intelligente** : Recherche par nom, email, entreprise, poste
- **Gestion avancée** :
  - Chronologie d'événements et échanges
  - Notes importantes
  - Prochaines actions avec échéances
  - Opportunités business avec valorisation
- **Statistiques** : Vue d'ensemble du réseau et des opportunités
- **Interface moderne** : Design responsive et intuitif

## 🛠️ Technologies

- **Backend** : FastAPI + Python 3
- **Base de données** : SQLite avec colonnes JSON
- **Frontend** : HTML5 + CSS3 + JavaScript vanilla
- **ORM** : SQLAlchemy

## 📋 Structure du Projet

```
webapp/
├── main.py              # Application FastAPI principale
├── database.py          # Configuration SQLite et modèles
├── models.py            # Modèles Pydantic pour validation
├── init_db.py          # Script d'initialisation de la base
├── requirements.txt     # Dépendances Python
├── contacts.db         # Base de données SQLite (créée automatiquement)
├── static/
│   ├── styles.css      # Styles CSS modernes
│   └── app.js          # Logique JavaScript
└── templates/
    └── index.html      # Interface utilisateur
```

## 🚀 Installation et Démarrage

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données avec l'exemple

```bash
python init_db.py
```

### 3. Démarrer l'application

```bash
python main.py
```

ou avec uvicorn directement :

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Séquence de démarrage

1. python main.py
2. FastAPI app créée
3. Uvicorn démarre
4. 🔥 Event "startup" déclenché
   ├─ init_db() s'exécute
   └─ get_version_info() récupère Git infos
5. app.state.version_info stocké en mémoire
6. ✅ Serveur prêt
7. Traite les requêtes (GET /, GET /api/contacts, etc.)

### 4. Accéder à l'application

- **Interface Web** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **API alternative** : http://localhost:8000/redoc

## 📡 API Endpoints

### Contacts

- `POST /api/contacts` - Créer un nouveau contact
- `GET /api/contacts` - Récupérer tous les contacts (avec recherche optionnelle)
- `GET /api/contacts/{contact_id}` - Récupérer un contact spécifique
- `PUT /api/contacts/{contact_id}` - Mettre à jour un contact
- `DELETE /api/contacts/{contact_id}` - Supprimer un contact

### Statistiques

- `GET /api/stats` - Obtenir les statistiques globales

## 📊 Format de Données

```json
{
  "contactId": "uuid...",
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
```

## 🎨 Fonctionnalités Interface

- **Dashboard** : Vue d'ensemble avec statistiques clés
- **Recherche en temps réel** : Filtre instantané des contacts
- **Cartes de contact** : Affichage élégant avec toutes les informations
- **Modal d'édition** : Formulaire complet pour créer/modifier
- **Listes dynamiques** : Ajout/suppression d'événements, notes, actions, opportunités
- **Design responsive** : S'adapte à tous les écrans

## 💾 Base de Données

La base SQLite (`contacts.db`) stocke les contacts avec :
- Champs texte simples : nom, email, entreprise, poste
- Colonnes JSON : événements, notes, actions, opportunités
- Index sur : contactId, nom, email, entreprise
- Timestamps automatiques

## 🔧 Développement

### Ajouter de nouvelles fonctionnalités

1. Modifier les modèles dans `models.py`
2. Mettre à jour le modèle de base de données dans `database.py`
3. Ajouter les endpoints dans `main.py`
4. Mettre à jour l'interface dans `templates/index.html` et `static/app.js`

### Tests API avec curl

```bash
# Lister les contacts
curl http://localhost:8000/api/contacts

# Créer un contact
curl -X POST http://localhost:8000/api/contacts \
  -H "Content-Type: application/json" \
  -d '{"nom":"Marie Martin","email":"marie@test.com","entreprise":"Test Corp"}'

# Rechercher
curl http://localhost:8000/api/contacts?search=Marie
```

## 📝 Notes

- Les données JSON sont stockées en colonnes TEXT avec sérialisation automatique
- Volumétrie optimisée pour quelques dizaines à centaines de contacts
- Pas d'authentification (à ajouter pour production)
- Backup simple : copier le fichier `data/contacts.db`

## 🚀 Améliorations Possibles

- [ ] Authentification utilisateur
- [ ] Export CSV/Excel
- [ ] Import de contacts
- [ ] Tags et catégories
- [ ] Rappels automatiques
- [ ] Intégration email
- [ ] Synchronisation cloud

## 📄 Licence

Projet personnel - Libre d'utilisation

---

**Développé avec ❤️ pour optimiser votre réseau business**
