// Main JavaScript - Navigation, Flash Messages, Mobile Menu

// Mobile Menu Toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Close Flash Messages
document.querySelectorAll('.close-alert').forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.style.display = 'none';
    });
});

// Auto-hide flash messages after 5 seconds
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    });
}, 5000);

// Shopping Cart functionality
const cart = {
    items: JSON.parse(localStorage.getItem('cart')) || [],
    
    add(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity += product.quantity;
        } else {
            this.items.push(product);
        }
        this.save();
        this.updateCount();
    },
    
    remove(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.save();
        this.updateCount();
    },
    
    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = quantity;
            if (item.quantity <= 0) {
                this.remove(productId);
            } else {
                this.save();
            }
        }
    },
    
    save() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    },
    
    updateCount() {
        const count = this.items.reduce((sum, item) => sum + item.quantity, 0);
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = count;
        }
    },
    
    getTotal() {
        return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },
    
    clear() {
        this.items = [];
        this.save();
        this.updateCount();
    }
};

// Initialize cart count on page load
cart.updateCount();

// Newsletter Form
const newsletterForm = document.getElementById('newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = e.target.querySelector('input[type="email"]').value;
        
        try {
            const response = await fetch('/api/newsletter/subscribe', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email })
            });
            
            if (response.ok) {
                showAlert('Thanks for subscribing!', 'success');
                e.target.reset();
            } else {
                showAlert('Subscription failed. Please try again.', 'error');
            }
        } catch (error) {
            showAlert('Error subscribing. Please try again later.', 'error');
        }
    });
}

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        ${message}
        <button class="close-alert">&times;</button>
    `;
    
    let container = document.querySelector('.flash-messages');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
    }
    
    container.appendChild(alertDiv);
    
    // Add close functionality
    alertDiv.querySelector('.close-alert').addEventListener('click', () => {
        alertDiv.remove();
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

// Export cart for use in other scripts
window.cart = cart;
window.showAlert = showAlert;
