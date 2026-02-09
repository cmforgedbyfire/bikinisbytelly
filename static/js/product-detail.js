// Product Detail Page - Image gallery, Add to cart, Reviews

// Image Gallery
function changeMainImage(src) {
    document.getElementById('main-product-image').src = src;
}

// Size selection - show custom measurements if needed
const sizeSelect = document.getElementById('size-select');
const customMeasurements = document.getElementById('custom-measurements');

if (sizeSelect) {
    sizeSelect.addEventListener('change', (e) => {
        if (e.target.value === 'custom') {
            customMeasurements.style.display = 'block';
        } else {
            customMeasurements.style.display = 'none';
        }
    });
}

// Color swatch selection
document.querySelectorAll('.color-swatch').forEach(swatch => {
    swatch.addEventListener('click', function() {
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
        this.classList.add('active');
    });
});

// Add to Cart
const addToCartBtn = document.getElementById('add-to-cart');
if (addToCartBtn) {
    addToCartBtn.addEventListener('click', async () => {
        const size = document.getElementById('size-select').value;
        const quantity = parseInt(document.getElementById('quantity').value);
        
        if (!size) {
            showAlert('Please select a size', 'error');
            return;
        }
        
        if (size === 'custom') {
            const bust = document.getElementById('bust').value;
            const waist = document.getElementById('waist').value;
            const hips = document.getElementById('hips').value;
            
            if (!bust || !waist || !hips) {
                showAlert('Please provide all custom measurements', 'error');
                return;
            }
        }
        
        // Get product data from page
        const productName = document.querySelector('.product-info h1').textContent;
        const productPrice = parseFloat(document.querySelector('.product-price').textContent.replace('$', ''));
        const productImage = document.getElementById('main-product-image').src;
        
        // Get selected color if any
        const selectedColor = document.querySelector('.color-swatch.active');
        const color = selectedColor ? selectedColor.dataset.color : null;
        
        // Create product object
        const product = {
            id: window.location.pathname.split('/').pop(),
            name: productName,
            price: productPrice,
            image: productImage,
            size: size,
            color: color,
            quantity: quantity
        };
        
        // Add custom measurements if applicable
        if (size === 'custom') {
            product.measurements = {
                bust: document.getElementById('bust').value,
                waist: document.getElementById('waist').value,
                hips: document.getElementById('hips').value
            };
        }
        
        // Add to cart
        cart.add(product);
        showAlert('Added to cart!', 'success');
    });
}

// Product Tabs
document.querySelectorAll('.tab-header').forEach(header => {
    header.addEventListener('click', function() {
        const tabName = this.dataset.tab;
        
        // Update active states
        document.querySelectorAll('.tab-header').forEach(h => h.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        this.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Load Reviews
async function loadReviews() {
    const productId = window.location.pathname.split('/').pop();
    try {
        const response = await fetch(`/api/products/${productId}/reviews`);
        const reviews = await response.json();
        
        const container = document.getElementById('reviews-container');
        if (reviews.length === 0) {
            container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        } else {
            container.innerHTML = reviews.map(review => `
                <div class="review">
                    <div class="review-header">
                        <strong>${review.name}</strong>
                        <span class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
                    </div>
                    <p>${review.review}</p>
                    <small>${new Date(review.created_at).toLocaleDateString()}</small>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

// Submit Review
const reviewForm = document.getElementById('review-form');
if (reviewForm) {
    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);
        
        try {
            const response = await fetch('/api/reviews', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                showAlert('Thank you for your review!', 'success');
                e.target.reset();
                loadReviews(); // Reload reviews
            } else {
                showAlert('Failed to submit review. Please try again.', 'error');
            }
        } catch (error) {
            showAlert('Error submitting review.', 'error');
        }
    });
}

// Load reviews on page load
if (document.getElementById('reviews-container')) {
    loadReviews();
}
