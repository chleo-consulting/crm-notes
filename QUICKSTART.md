# Guide de Démarrage Rapide 🚀

## Démarrage en 3 étapes

### 1️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialiser la base de données (si besoin)
```bash
python init_db.py
```

### 3️⃣ Démarrer l'application
```bash
# Option 1 : Script automatique
./start.sh

# Option 2 : Commande directe
python main.py
```

## Accès à l'application

- **Interface Web** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **API Redoc** : http://localhost:8000/redoc

## Utilisation de l'interface

### Créer un contact
1. Cliquez sur "➕ Nouveau Contact"
2. Remplissez les informations du contact
3. Ajoutez des événements, notes, actions et opportunités avec les boutons "+"
4. Cliquez sur "💾 Enregistrer"

### Rechercher un contact
- Utilisez la barre de recherche en haut
- La recherche fonctionne sur : nom, email, entreprise, poste

### Modifier un contact
- Cliquez sur l'icône ✏️ sur la fiche du contact
- Modifiez les informations souhaitées
- Enregistrez les modifications

### Supprimer un contact
- Cliquez sur l'icône 🗑️ sur la fiche du contact
- Confirmez la suppression

## Exemples d'utilisation de l'API

### Lister tous les contacts
```bash
curl http://localhost:8000/api/contacts
```

### Créer un contact
```bash
curl -X POST http://localhost:8000/api/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Marie Martin",
    "email": "marie.martin@example.com",
    "entreprise": "TechCorp",
    "poste": "Directrice Commerciale",
    "evenements": [
      {
        "date": "2026-01-20T10:00:00Z",
        "type": "réunion",
        "notes": "Présentation de notre solution"
      }
    ],
    "notesImportantes": ["Décisionnaire clé", "Budget disponible Q1"],
    "prochainesActions": [
      {
        "action": "Envoyer devis personnalisé",
        "dateEcheance": "2026-01-25"
      }
    ],
    "opportunites": [
      {
        "projet": "Transformation digitale 2026",
        "valeurEstimee": 50000
      }
    ]
  }'
```

### Rechercher des contacts
```bash
curl "http://localhost:8000/api/contacts?search=Marie"
```

### Obtenir les statistiques
```bash
curl http://localhost:8000/api/stats
```

### Récupérer un contact spécifique
```bash
curl http://localhost:8000/api/contacts/{contactId}
```

### Mettre à jour un contact
```bash
curl -X PUT http://localhost:8000/api/contacts/{contactId} \
  -H "Content-Type: application/json" \
  -d '{
    "poste": "Directrice Générale"
  }'
```

### Supprimer un contact
```bash
curl -X DELETE http://localhost:8000/api/contacts/{contactId}
```

## Structure des données

Chaque contact contient :
- **Informations de base** : nom, email, entreprise, poste
- **Événements** : chronologie des interactions (appels, réunions, emails)
- **Notes importantes** : informations clés à retenir
- **Prochaines actions** : tâches à effectuer avec échéances
- **Opportunités** : projets potentiels avec valorisation

## Conseils d'utilisation

✅ **Bonnes pratiques** :
- Mettez à jour régulièrement vos contacts après chaque interaction
- Utilisez les événements pour garder une trace de votre historique
- Planifiez vos prochaines actions pour ne rien oublier
- Estimez la valeur des opportunités pour prioriser vos efforts

📊 **Suivi de votre réseau** :
- Consultez le dashboard pour voir l'évolution de votre réseau
- Surveillez la valeur totale de vos opportunités
- Utilisez la recherche pour retrouver rapidement un contact

## Sauvegarde des données

Votre base de données est dans le fichier `data/contacts.db`.

Pour sauvegarder vos données :
```bash
# Copier la base de données
cp data/contacts.db backup/contacts_backup_$(date +%Y%m%d).db
```

Pour restaurer une sauvegarde :
```bash
# Restaurer une ancienne version
cp backup/contacts_backup_20260120.db data/contacts.db
```

## Arrêter l'application

Appuyez sur `Ctrl+C` dans le terminal où le serveur est en cours d'exécution.

## Support et Documentation

- Pour plus de détails, consultez le [README.md](README.md)
- Documentation API interactive : http://localhost:8000/docs

---

**Bon réseautage ! 🎯**
