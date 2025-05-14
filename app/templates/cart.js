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

function updateTotal() {
    let total = 0;
    const items = document.querySelectorAll('.cart-item');
    items.forEach(item => {
        const priceText = item.querySelector('.item-price')?.textContent;
        if (priceText) {
            const price = parseFloat(priceText.replace(',', '.').replace('€', '').trim());
            if (!isNaN(price)) total += price;
        }
    });

    const totalElement = document.getElementById('total-amount');
    const checkoutForm = document.getElementById('checkout-button');
    const emptyMessage = document.getElementById('empty-message');

    if (items.length === 0) {
        // Si plus d'articles, on cache le total et le bouton
        if (totalElement) totalElement.style.display = 'none';
        if (checkoutForm) checkoutForm.style.display = 'none';
        if (emptyMessage) emptyMessage.style.display = 'block';
    } else {
        // Sinon on met à jour le total
        if (totalElement) {
            totalElement.textContent = `Total : ${total.toFixed(2)} €`;
            totalElement.style.display = 'block';
        }
        if (checkoutForm) checkoutForm.style.display = 'block';
        if (emptyMessage) emptyMessage.style.display = 'none';
    }
}

