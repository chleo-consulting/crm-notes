// app.js - Logique JavaScript pour l'interface de gestion de contacts

class ContactManager {
    constructor() {
        this.contacts = [];
        this.currentContact = null;
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadContacts();
        await this.loadStats();
    }

    setupEventListeners() {
        // Bouton nouveau contact
        document.getElementById('newContactBtn').addEventListener('click', () => {
            this.openModal();
        });

        // Recherche
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.searchContacts(e.target.value);
        });

        // Fermeture modale
        document.getElementById('closeModal').addEventListener('click', () => {
            this.closeModal();
        });

        // Clic en dehors de la modale
        document.getElementById('contactModal').addEventListener('click', (e) => {
            if (e.target.id === 'contactModal') {
                this.closeModal();
            }
        });

        // Soumission du formulaire
        document.getElementById('contactForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveContact();
        });

        // Boutons pour ajouter des éléments
        document.getElementById('addEventBtn').addEventListener('click', () => this.addEventField());
        document.getElementById('addNoteBtn').addEventListener('click', () => this.addNoteField());
        document.getElementById('addActionBtn').addEventListener('click', () => this.addActionField());
        document.getElementById('addOpportunityBtn').addEventListener('click', () => this.addOpportunityField());
    }

    async loadContacts(search = '') {
        try {
            const url = search ? `/api/contacts?search=${encodeURIComponent(search)}` : '/api/contacts';
            const response = await fetch(url);
            this.contacts = await response.json();
            this.renderContacts();
        } catch (error) {
            console.error('Erreur lors du chargement des contacts:', error);
            this.showError('Erreur lors du chargement des contacts');
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            document.getElementById('totalContacts').textContent = stats.totalContacts;
            document.getElementById('totalOpportunites').textContent = stats.totalOpportunites;
            document.getElementById('valeurTotale').textContent = 
                new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(stats.valeurTotaleOpportunites);
        } catch (error) {
            console.error('Erreur lors du chargement des statistiques:', error);
        }
    }

    renderContacts() {
        const container = document.getElementById('contactsContainer');
        
        if (this.contacts.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                    <div style="font-size: 3rem; margin-bottom: 20px;">📇</div>
                    <h3 style="color: var(--text-secondary); margin-bottom: 10px;">Aucun contact</h3>
                    <p style="color: var(--text-secondary);">Commencez par créer votre premier contact</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.contacts.map(contact => `
            <div class="contact-card" data-id="${contact.contactId}">
                <div class="contact-header">
                    <div>
                        <h3>${this.escapeHtml(contact.nom)}</h3>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">${this.escapeHtml(contact.poste || '')}</p>
                    </div>
                    <div class="contact-actions">
                        <button class="btn-icon" onclick="contactManager.editContact('${contact.contactId}')" title="Modifier">✏️</button>
                        <button class="btn-icon" onclick="contactManager.deleteContact('${contact.contactId}')" title="Supprimer">🗑️</button>
                    </div>
                </div>
                
                <div class="contact-info">
                    ${contact.email ? `<p><strong>📧</strong> ${this.escapeHtml(contact.email)}</p>` : ''}
                    ${contact.entreprise ? `<p><strong>🏢</strong> ${this.escapeHtml(contact.entreprise)}</p>` : ''}
                </div>

                ${contact.evenements && contact.evenements.length > 0 ? `
                    <div class="contact-section">
                        <h4>📅 Derniers événements</h4>
                        ${contact.evenements.slice(0, 2).map(e => `
                            <div style="margin-bottom: 8px;">
                                <span class="badge badge-primary">${e.type}</span>
                                <span style="font-size: 0.85rem; color: var(--text-secondary);">${this.formatDate(e.date)}</span>
                                <p style="font-size: 0.85rem; margin-top: 4px;">${this.escapeHtml(e.notes)}</p>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}

                ${contact.notesImportantes && contact.notesImportantes.length > 0 ? `
                    <div class="contact-section">
                        <h4>📝 Notes importantes</h4>
                        ${contact.notesImportantes.slice(0, 2).map(note => `
                            <p style="font-size: 0.85rem; margin-bottom: 5px;">• ${this.escapeHtml(note)}</p>
                        `).join('')}
                    </div>
                ` : ''}

                ${contact.prochainesActions && contact.prochainesActions.length > 0 ? `
                    <div class="contact-section">
                        <h4>✅ Prochaines actions</h4>
                        ${contact.prochainesActions.slice(0, 2).map(action => `
                            <div style="margin-bottom: 8px;">
                                <span class="badge badge-warning">${this.formatDate(action.dateEcheance)}</span>
                                <p style="font-size: 0.85rem; margin-top: 4px;">${this.escapeHtml(action.action)}</p>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}

                ${contact.opportunites && contact.opportunites.length > 0 ? `
                    <div class="contact-section">
                        <h4>💰 Opportunités</h4>
                        ${contact.opportunites.map(opp => `
                            <div style="margin-bottom: 8px;">
                                <p style="font-size: 0.85rem;"><strong>${this.escapeHtml(opp.projet)}</strong></p>
                                ${opp.valeurEstimee ? `<span class="badge badge-success">${new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(opp.valeurEstimee)}</span>` : ''}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    openModal(contact = null) {
        this.currentContact = contact;
        const modal = document.getElementById('contactModal');
        const form = document.getElementById('contactForm');
        
        form.reset();
        document.getElementById('modalTitle').textContent = contact ? 'Modifier le contact' : 'Nouveau contact';
        
        // Vider les listes dynamiques
        document.getElementById('evenementsList').innerHTML = '';
        document.getElementById('notesList').innerHTML = '';
        document.getElementById('actionsList').innerHTML = '';
        document.getElementById('opportunitesList').innerHTML = '';
        
        if (contact) {
            // Remplir le formulaire avec les données existantes
            document.getElementById('nom').value = contact.nom || '';
            document.getElementById('email').value = contact.email || '';
            document.getElementById('entreprise').value = contact.entreprise || '';
            document.getElementById('poste').value = contact.poste || '';
            
            // Ajouter les événements
            contact.evenements?.forEach(e => this.addEventField(e));
            
            // Ajouter les notes
            contact.notesImportantes?.forEach(note => this.addNoteField(note));
            
            // Ajouter les actions
            contact.prochainesActions?.forEach(action => this.addActionField(action));
            
            // Ajouter les opportunités
            contact.opportunites?.forEach(opp => this.addOpportunityField(opp));
        }
        
        modal.classList.add('active');
    }

    closeModal() {
        document.getElementById('contactModal').classList.remove('active');
        this.currentContact = null;
    }

    addEventField(data = null) {
        const container = document.getElementById('evenementsList');
        const id = Date.now();
        const html = `
            <div class="list-item" data-id="${id}">
                <input type="date" placeholder="Date" value="${data?.date?.split('T')[0] || ''}" data-field="date" required>
                <input type="text" placeholder="Type" value="${data?.type || ''}" data-field="type" required>
                <input type="text" placeholder="Notes" value="${data?.notes || ''}" data-field="notes" required>
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()">✕</button>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
    }

    addNoteField(data = null) {
        const container = document.getElementById('notesList');
        const id = Date.now();
        const html = `
            <div class="list-item" data-id="${id}">
                <input type="text" placeholder="Note importante" value="${data || ''}" data-field="note" required>
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()">✕</button>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
    }

    addActionField(data = null) {
        const container = document.getElementById('actionsList');
        const id = Date.now();
        const html = `
            <div class="list-item" data-id="${id}">
                <input type="text" placeholder="Action" value="${data?.action || ''}" data-field="action" required>
                <input type="date" placeholder="Date échéance" value="${data?.dateEcheance?.split('T')[0] || ''}" data-field="dateEcheance" required>
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()">✕</button>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
    }

    addOpportunityField(data = null) {
        const container = document.getElementById('opportunitesList');
        const id = Date.now();
        const html = `
            <div class="list-item" data-id="${id}">
                <input type="text" placeholder="Projet" value="${data?.projet || ''}" data-field="projet" required>
                <input type="number" placeholder="Valeur (€)" value="${data?.valeurEstimee || ''}" data-field="valeurEstimee" step="0.01">
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()">✕</button>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
    }

    async saveContact() {
        const formData = {
            nom: document.getElementById('nom').value,
            email: document.getElementById('email').value || null,
            entreprise: document.getElementById('entreprise').value || null,
            poste: document.getElementById('poste').value || null,
            evenements: this.getListData('evenementsList', ['date', 'type', 'notes']),
            notesImportantes: this.getListData('notesList', ['note'], true),
            prochainesActions: this.getListData('actionsList', ['action', 'dateEcheance']),
            opportunites: this.getListData('opportunitesList', ['projet', 'valeurEstimee'])
        };

        try {
            let response;
            if (this.currentContact) {
                // Mise à jour
                response = await fetch(`/api/contacts/${this.currentContact.contactId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
            } else {
                // Création
                response = await fetch('/api/contacts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
            }

            if (response.ok) {
                this.closeModal();
                await this.loadContacts();
                await this.loadStats();
                this.showSuccess(this.currentContact ? 'Contact modifié avec succès' : 'Contact créé avec succès');
            } else {
                throw new Error('Erreur lors de la sauvegarde');
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.showError('Erreur lors de la sauvegarde du contact');
        }
    }

    getListData(containerId, fields, singleValue = false) {
        const container = document.getElementById(containerId);
        const items = container.querySelectorAll('.list-item');
        
        return Array.from(items).map(item => {
            if (singleValue) {
                return item.querySelector(`[data-field="${fields[0]}"]`).value;
            }
            
            const obj = {};
            fields.forEach(field => {
                const input = item.querySelector(`[data-field="${field}"]`);
                let value = input.value;
                
                // Conversion des nombres
                if (input.type === 'number' && value) {
                    value = parseFloat(value);
                }
                
                // Conversion des dates en ISO
                if (input.type === 'date' && value) {
                    value = new Date(value).toISOString();
                }
                
                obj[field] = value || (input.type === 'number' ? null : '');
            });
            return obj;
        });
    }

    async editContact(contactId) {
        try {
            const response = await fetch(`/api/contacts/${contactId}`);
            const contact = await response.json();
            this.openModal(contact);
        } catch (error) {
            console.error('Erreur:', error);
            this.showError('Erreur lors du chargement du contact');
        }
    }

    async deleteContact(contactId) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer ce contact ?')) {
            return;
        }

        try {
            const response = await fetch(`/api/contacts/${contactId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                await this.loadContacts();
                await this.loadStats();
                this.showSuccess('Contact supprimé avec succès');
            } else {
                throw new Error('Erreur lors de la suppression');
            }
        } catch (error) {
            console.error('Erreur:', error);
            this.showError('Erreur lors de la suppression du contact');
        }
    }

    async searchContacts(query) {
        await this.loadContacts(query);
    }

    formatDate(dateStr) {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return new Intl.DateTimeFormat('fr-FR', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        }).format(date);
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showSuccess(message) {
        // Simple alert pour l'instant
        alert('✅ ' + message);
    }

    showError(message) {
        // Simple alert pour l'instant
        alert('❌ ' + message);
    }
}

// Initialisation au chargement de la page
let contactManager;
document.addEventListener('DOMContentLoaded', () => {
    contactManager = new ContactManager();
});
