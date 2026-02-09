// Shopping Cart
const cart = {
    items: JSON.parse(localStorage.getItem('cart')) || [],
    
    add(product) {
        const existing = this.items.find(item => 
            item.id === product.id && item.size === product.size
        );
        
        if (existing) {
            existing.quantity += product.quantity || 1;
        } else {
            this.items.push({
                id: product.id,
                name: product.name,
                price: product.price,
                size: product.size || 'M',
                quantity: product.quantity || 1,
                image: product.image
            });
        }
        
        this.save();
        this.updateUI();
        this.showNotification(`${product.name} added to cart!`);
    },
    
    remove(index) {
        this.items.splice(index, 1);
        this.save();
        this.updateUI();
    },
    
    updateQuantity(index, quantity) {
        if (quantity <= 0) {
            this.remove(index);
        } else {
            this.items[index].quantity = quantity;
            this.save();
            this.updateUI();
        }
    },
    
    clear() {
        this.items = [];
        this.save();
        this.updateUI();
    },
    
    getTotal() {
        return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },
    
    save() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    },
    
    updateUI() {
        const countElements = document.querySelectorAll('.cart-count');
        const count = this.items.reduce((sum, item) => sum + item.quantity, 0);
        countElements.forEach(el => el.textContent = count);
    },
    
    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'cart-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: var(--ocean-blue);
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }
};

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Update cart count on page load
    cart.updateUI();
    
    // Add to Cart Buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (e) => {
            const productCard = e.target.closest('.product-card');
            const productId = productCard.dataset.product;
            const productName = productCard.querySelector('h3').textContent;
            const productPrice = parseFloat(
                productCard.querySelector('.product-price')
                    .textContent.replace('$', '')
            );
            const productImage = productCard.querySelector('img').src;
            
            cart.add({
                id: productId,
                name: productName,
                price: productPrice,
                image: productImage,
                size: 'M'  // Default size
            });
        });
    });
    
    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Hero Scroll Button
    const heroScroll = document.querySelector('.hero-scroll');
    if (heroScroll) {
        heroScroll.addEventListener('click', () => {
            window.scrollTo({
                top: window.innerHeight,
                behavior: 'smooth'
            });
        });
    }
});

// Add animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Export cart for use in other pages
window.cart = cart;
