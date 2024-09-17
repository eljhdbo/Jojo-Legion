// personnages.js

document.addEventListener("DOMContentLoaded", function () {
    const listePersonnages = document.getElementById('liste-personnages');
    const rechercheInput = document.getElementById('recherche');
    const partieSelect = document.getElementById('partie');
    const paginationDiv = document.getElementById('pagination');

    let personnages = [];  // Liste des personnages récupérés de l'API
    let pageActuelle = 1;  // Page actuelle
    const personnagesParPage = 10;  // Nombre de personnages par page

    // Fonction pour récupérer les personnages de l'API
    async function obtenirPersonnages() {
        try {
            // Remplacez l'URL ci-dessous par l'URL de votre API
            const reponse = await fetch('https://api.example.com/personnages');
            personnages = await reponse.json();
            afficherPersonnages();
            genererPagination();
        } catch (erreur) {
            console.error('Erreur lors de la récupération des personnages :', erreur);
        }
    }

    // Fonction pour afficher les personnages dans la liste
    function afficherPersonnages() {
        const personnagesFiltrés = filtrerPersonnages();
        const debut = (pageActuelle - 1) * personnagesParPage;
        const fin = debut + personnagesParPage;
        const personnagesAffichés = personnagesFiltrés.slice(debut, fin);

        listePersonnages.innerHTML = '';
        personnagesAffichés.forEach(personnage => {
            const carte = document.createElement('div');
            carte.classList.add('carte-personnage');

            carte.innerHTML = `
                <img src="${personnage.image}" alt="Image de ${personnage.nom}">
                <h3>${personnage.nom}</h3>
                <p>${personnage.description}</p>
                <p><strong>Partie:</strong> ${personnage.partie}</p>
            `;

            listePersonnages.appendChild(carte);
        });
    }

    // Fonction pour filtrer les personnages
    function filtrerPersonnages() {
        const termeRecherche = rechercheInput.value.toLowerCase();
        const partieFiltrée = partieSelect.value;

        return personnages.filter(personnage => {
            const correspondRecherche = personnage.nom.toLowerCase().includes(termeRecherche);
            const correspondPartie = partieFiltrée === '' || personnage.partie === partieFiltrée;
            return correspondRecherche && correspondPartie;
        });
    }

    // Fonction pour générer la pagination
    function genererPagination() {
        const personnagesFiltrés = filtrerPersonnages();
        const nombrePages = Math.ceil(personnagesFiltrés.length / personnagesParPage);

        paginationDiv.innerHTML = '';
        for (let i = 1; i <= nombrePages; i++) {
            const bouton = document.createElement('button');
            bouton.textContent = i;
            bouton.className = (i === pageActuelle) ? 'actif' : '';
            bouton.addEventListener('click', function () {
                pageActuelle = i;
                afficherPersonnages();
                genererPagination();
            });
            paginationDiv.appendChild(bouton);
        }
    }

    // Appeler la fonction pour récupérer et afficher les personnages
    obtenirPersonnages();
});
