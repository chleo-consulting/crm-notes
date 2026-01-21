#!/bin/bash

# Script de démarrage de l'application Gestionnaire de Contacts Business

echo "🚀 Démarrage du Gestionnaire de Contacts Business..."
echo ""

# Vérifier si les dépendances sont installées
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installation des dépendances..."
    pip install -r requirements.txt
    echo ""
fi

# Vérifier si la base de données existe
if [ ! -f "contacts.db" ]; then
    echo "🗄️  Initialisation de la base de données..."
    python init_db.py
    echo ""
fi

echo "✅ Prêt à démarrer !"
echo ""
echo "🌐 L'application sera accessible sur : http://localhost:8000"
echo "📚 Documentation API : http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Démarrer le serveur
python main.py
