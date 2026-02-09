// Shopping Cart Page

document.addEventListener('DOMContentLoaded', () => {
    loadCart();
});

function loadCart() {
    const cartContent = document.getElementById('cart-content');
    const items = cart.items;
    
    if (items.length === 0) {
        cartContent.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart" style="font-size: 4rem; color: var(--text-light);"></i>
                <h2>Your cart is empty</h2>
                <p>Add some beautiful bikinis to get started!</p>
                <a href="/products" class="btn btn-primary">Shop Now</a>
            </div>
        `;
        updateCartTotals(0, 0, 0);
        return;
    }
    
    cartContent.innerHTML = items.map(item => `
        <div class="cart-item" data-id="${item.id}">
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <h3>${item.name}</h3>
                <p>Size: ${item.size}</p>
                ${item.color ? `<p>Color: ${item.color}</p>` : ''}
                ${item.measurements ? `<p>Custom Measurements</p>` : ''}
                <p class="item-price">$${item.price.toFixed(2)} each</p>
                <div class="quantity-selector">
                    <button onclick="updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
                    <input type="number" value="${item.quantity}" min="1" 
                           onchange="updateQuantity('${item.id}', this.value)">
                    <button onclick="updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
                </div>
            </div>
            <div class="cart-item-actions">
                <p class="item-total">$${(item.price * item.quantity).toFixed(2)}</p>
                <button onclick="removeFromCart('${item.id}')" class="btn-remove">
                    <i class="fas fa-trash"></i> Remove
                </button>
            </div>
        </div>
    `).join('');
    
    calculateTotals();
}

function updateQuantity(productId, quantity) {
    quantity = parseInt(quantity);
    if (quantity < 1) return;
    cart.updateQuantity(productId, quantity);
    loadCart();
}

function removeFromCart(productId) {
    if (confirm('Remove this item from cart?')) {
        cart.remove(productId);
        loadCart();
        showAlert('Item removed from cart', 'info');
    }
}

function calculateTotals() {
    const subtotal = cart.getTotal();
    const shipping = subtotal >= 100 ? 0 : 10; // Free shipping over $100
    const tax = subtotal * 0.08; // 8% tax (adjust as needed)
    const total = subtotal + shipping + tax;
    
    updateCartTotals(subtotal, shipping, tax, total);
}

function updateCartTotals(subtotal, shipping, tax, total) {
    document.getElementById('cart-subtotal').textContent = `$${(subtotal || 0).toFixed(2)}`;
    document.getElementById('cart-shipping').textContent = 
        shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}`;
    document.getElementById('cart-tax').textContent = `$${(tax || 0).toFixed(2)}`;
    document.getElementById('cart-total').textContent = `$${(total || 0).toFixed(2)}`;
}

// Checkout Button
const checkoutBtn = document.getElementById('checkout-btn');
if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
        if (cart.items.length === 0) {
            showAlert('Your cart is empty', 'error');
            return;
        }
        window.location.href = '/checkout';
    });
}
