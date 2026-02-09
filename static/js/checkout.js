// Checkout Page with Stripe Integration

let stripe;
let cardElement;

document.addEventListener('DOMContentLoaded', async () => {
    loadCheckoutItems();
    initializeStripe();
    setupCheckoutForm();
});

function loadCheckoutItems() {
    const itemsContainer = document.getElementById('checkout-items');
    const items = cart.items;
    
    if (items.length === 0) {
        window.location.href = '/cart';
        return;
    }
    
    itemsContainer.innerHTML = items.map(item => `
        <div class="checkout-item">
            <img src="${item.image}" alt="${item.name}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;">
            <div>
                <strong>${item.name}</strong><br>
                <small>Size: ${item.size} | Qty: ${item.quantity}</small>
            </div>
            <span>$${(item.price * item.quantity).toFixed(2)}</span>
        </div>
    `).join('');
    
    calculateCheckoutTotals();
}

function calculateCheckoutTotals() {
    const subtotal = cart.getTotal();
    const shipping = subtotal >= 100 ? 0 : 10;
    const tax = subtotal * 0.08;
    const total = subtotal + shipping + tax;
    
    document.getElementById('checkout-subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('checkout-shipping').textContent = 
        shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}`;
    document.getElementById('checkout-tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('checkout-total').textContent = `$${total.toFixed(2)}`;
    
    return total;
}

async function initializeStripe() {
    try {
        // Fetch Stripe public key from server
        const response = await fetch('/api/stripe/public-key');
        const { publicKey } = await response.json();
        
        stripe = Stripe(publicKey);
        const elements = stripe.elements();
        
        cardElement = elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#2C3E50',
                    fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
                }
            }
        });
        
        cardElement.mount('#card-element');
        
        cardElement.on('change', (event) => {
            const displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });
    } catch (error) {
        console.error('Error initializing Stripe:', error);
        showAlert('Payment system error. Please try again later.', 'error');
    }
}

function setupCheckoutForm() {
    const form = document.getElementById('checkout-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = document.getElementById('submit-payment');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        
        try {
            // Get form data
            const formData = new FormData(form);
            const orderData = {
                customer: Object.fromEntries(formData),
                items: cart.items,
                total: calculateCheckoutTotals()
            };
            
            // Create payment intent
            const response = await fetch('/api/create-payment-intent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderData)
            });
            
            const { clientSecret, orderId } = await response.json();
            
            // Confirm payment with Stripe
            const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: `${orderData.customer.first_name} ${orderData.customer.last_name}`,
                        email: orderData.customer.email,
                        address: {
                            line1: orderData.customer.address,
                            line2: orderData.customer.address2,
                            city: orderData.customer.city,
                            state: orderData.customer.state,
                            postal_code: orderData.customer.zip
                        }
                    }
                }
            });
            
            if (error) {
                throw new Error(error.message);
            }
            
            if (paymentIntent.status === 'succeeded') {
                // Clear cart
                cart.clear();
                
                // Redirect to success page
                window.location.href = `/order-confirmation/${orderId}`;
            }
            
        } catch (error) {
            console.error('Payment error:', error);
            showAlert(error.message || 'Payment failed. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Complete Order';
        }
    });
}
