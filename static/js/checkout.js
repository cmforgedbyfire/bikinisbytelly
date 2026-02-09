// Checkout Page with PayPal Integration

document.addEventListener('DOMContentLoaded', async () => {
    loadCheckoutItems();
    initializePayPal();
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

function initializePayPal() {
    const form = document.getElementById('checkout-form');
    
    paypal.Buttons({
        createOrder: async function() {
            // Validate form first
            if (!form.checkValidity()) {
                form.reportValidity();
                throw new Error('Please fill in all required fields');
            }
            
            const formData = new FormData(form);
            const orderData = {
                customer: Object.fromEntries(formData),
                items: cart.items,
                totals: {
                    subtotal: cart.getTotal(),
                    shipping: cart.getTotal() >= 100 ? 0 : 10,
                    tax: cart.getTotal() * 0.08,
                    total: calculateCheckoutTotals()
                }
            };
            
            try {
                const response = await fetch('/api/paypal/create-payment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(orderData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    return data.payment_id;
                } else {
                    throw new Error(data.error || 'Payment creation failed');
                }
            } catch (error) {
                console.error('Error creating payment:', error);
                showAlert('Error creating payment. Please try again.', 'error');
                throw error;
            }
        },
        onApprove: async function(data) {
            try {
                const response = await fetch('/api/paypal/execute-payment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        payment_id: data.orderID,
                        payer_id: data.payerID
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    cart.clear();
                    window.location.href = `/order-confirmation/${result.order_id}`;
                } else {
                    showAlert('Payment failed. Please try again.', 'error');
                }
            } catch (error) {
                console.error('Error executing payment:', error);
                showAlert('Payment processing error. Please contact support.', 'error');
            }
        },
        onError: function(err) {
            console.error('PayPal error:', err);
            showAlert('Payment error. Please try again.', 'error');
        }
    }).render('#paypal-button-container');
}
