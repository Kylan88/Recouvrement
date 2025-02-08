document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('add-client-form').addEventListener('submit', addClient);
    document.getElementById('send-reminders').addEventListener('click', sendReminders); // Bouton de rappel manuel
    getClients();
});

// Fonction pour ajouter un client
async function addClient(event) {
    event.preventDefault(); // Empêche le rechargement de la page lors de l'envoi du formulaire

    const nameInput = document.getElementById('client-name');
    const phoneInput = document.getElementById('client-phone');
    const emailInput = document.getElementById('client-email');
    const montantInput = document.getElementById('client-montant');
    const dateEcheanceInput = document.getElementById('client-date-echeance');

    // Vérifie que tous les éléments existent
    if (!nameInput || !phoneInput || !emailInput || !montantInput || !dateEcheanceInput) {
        console.error('Un ou plusieurs champs du formulaire sont introuvables.');
        return;
    }

    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    const email = emailInput.value.trim();
    const montant = montantInput.value.trim();
    const dateEcheance = dateEcheanceInput.value;

    // Validation du montant
    if (!/^\d+(\.\d{1,2})?$/.test(montant)) {
        alert('Veuillez saisir un montant valide, par exemple 100 ou 100.50.');
        return;
    }
    const montantNum = parseFloat(montant);
    if (isNaN(montantNum) || montantNum <= 0) {
        alert('Le montant doit être supérieur à 0.');
        return;
    }

    // Validation des champs vides
    if (!name || !phone || !email || !dateEcheance) {
        alert('Veuillez remplir tous les champs correctement.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/clients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nom: name,
                telephone: phone,
                email: email,
                montant_du: montantNum,
                date_echeance: dateEcheance
            })
        });

        if (response.ok) {
            alert('Client ajouté avec succès !');
            document.getElementById('add-client-form').reset(); // Réinitialiser le formulaire
            getClients(); // Mettre à jour la liste des clients
        } else {
            const errorData = await response.json();
            alert(`Erreur: ${errorData.error || 'Impossible d\'ajouter le client'}`);
        }
    } catch (error) {
        console.error(error);
        alert('Une erreur s\'est produite. Veuillez réessayer.');
    }
}

// Fonction pour récupérer les clients et les afficher
async function getClients() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/clients');
        const clients = await response.json();
        const clientList = document.getElementById('client-list');

        // Vider la liste avant de la remplir
        clientList.innerHTML = '';

        clients.forEach(client => {
            const clientItem = document.createElement('a');
            clientItem.href = "#";
            clientItem.textContent = `${client.nom} (${client.telephone}) - ${client.email} - Montant dû: ${client.montant_du} - Échéance: ${client.date_echeance}`;
            clientList.appendChild(clientItem);
        });
    } catch (error) {
        console.error('Erreur lors de la récupération des clients:', error);
    }
}


// Fonction pour déclencher manuellement les rappels
async function sendReminders() {
    const statusDiv = document.getElementById('reminders-status');
    statusDiv.textContent = "Envoi des rappels en cours...";
    try {
        const response = await fetch('http://127.0.0.1:5000/api/rappels', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            const result = await response.json();
            statusDiv.textContent = resu
            lt.message; // Affiche le message sur la page
        } else {
            const errorData = await response.json();
            statusDiv.textContent = `Erreur: ${errorData.error || 'Impossible d\'envoyer les rappels.'}`;
        }
    } catch (error) {
        statusDiv.textContent = "Une erreur s'est produite. Veuillez réessayer.";
        console.error(error);
    }
}

