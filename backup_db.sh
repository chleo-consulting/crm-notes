#!/bin/bash

#######################################################
# Script de sauvegarde automatique de la base de données
# Usage: ./backup_db.sh
#######################################################

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_FILE="$SCRIPT_DIR/data/contacts.db"
BACKUP_DIR="$SCRIPT_DIR/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/contacts_backup_$TIMESTAMP.db"

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Vérifier que la base de données existe
if [ ! -f "$DB_FILE" ]; then
    log_error "La base de données n'existe pas: $DB_FILE"
    exit 1
fi

# Créer le répertoire de backup s'il n'existe pas
if [ ! -d "$BACKUP_DIR" ]; then
    log_info "Création du répertoire de backup: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# Afficher les informations
log_info "Démarrage de la sauvegarde..."
log_info "Base source: $DB_FILE"
log_info "Destination: $BACKUP_FILE"

# Copier la base de données
if cp "$DB_FILE" "$BACKUP_FILE"; then
    # Obtenir la taille du fichier
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log_info "✅ Sauvegarde réussie!"
    log_info "Fichier créé: $BACKUP_FILE"
    log_info "Taille: $SIZE"
    
    # Compter le nombre de backups existants
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/contacts_backup_*.db 2>/dev/null | wc -l)
    log_info "Nombre total de sauvegardes: $BACKUP_COUNT"
    
    # Optionnel: Supprimer les backups de plus de 30 jours
    log_info "Nettoyage des anciennes sauvegardes (> 30 jours)..."
    OLD_BACKUPS=$(find "$BACKUP_DIR" -name "contacts_backup_*.db" -type f -mtime +30)
    if [ -n "$OLD_BACKUPS" ]; then
        echo "$OLD_BACKUPS" | while read -r old_file; do
            log_warning "Suppression: $(basename "$old_file")"
            rm -f "$old_file"
        done
    else
        log_info "Aucune sauvegarde ancienne à supprimer"
    fi
    
    exit 0
else
    log_error "❌ Échec de la sauvegarde!"
    exit 1
fi