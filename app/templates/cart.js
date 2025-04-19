// cart.js

// Fonction pour ajouter un article au panier
function addToCart(offerId) {
    fetch(`/add_to_cart/${offerId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Mettre à jour l'UI avec le nombre d'articles dans le panier
        document.getElementById('cart-count').textContent = data.cartCount;
    })
    .catch(error => console.error('Erreur:', error));
}

// Fonction pour retirer un article du panier
function removeFromCart(offerId) {
    fetch(`/remove_from_cart/${offerId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Mettre à jour l'UI avec le nouveau nombre d'articles dans le panier
        document.getElementById('cart-count').textContent = data.cartCount;
    })
    .catch(error => console.error('Erreur:', error));
}
