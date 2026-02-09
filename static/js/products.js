// Products Page - Filtering, Sorting, and Display

let allProducts = [];
let filteredProducts = [];

// Load products on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadProducts();
    setupFilters();
    setupSort();
});

async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        allProducts = await response.json();
        filteredProducts = [...allProducts];
        displayProducts(filteredProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('products-grid').innerHTML = 
            '<p class="text-center">Error loading products. Please try again later.</p>';
    }
}

function displayProducts(products) {
    const grid = document.getElementById('products-grid');
    const countEl = document.getElementById('product-count');
    
    countEl.textContent = products.length;
    
    if (products.length === 0) {
        grid.innerHTML = '<p class="text-center">No products found matching your filters.</p>';
        return;
    }
    
    grid.innerHTML = products.map(product => `
        <div class="product-card">
            <a href="/product/${product.id}">
                <img src="${product.image || '/static/images/placeholder.jpg'}" alt="${product.name}">
            </a>
            <h3>${product.name}</h3>
            <p class="price">$${product.price.toFixed(2)}</p>
            <a href="/product/${product.id}" class="btn btn-secondary">View Details</a>
        </div>
    `).join('');
}

function setupFilters() {
    // Style filters
    document.querySelectorAll('input[name="style"]').forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
    
    // Color filters
    document.querySelectorAll('input[name="color"]').forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
    
    // Price filters
    document.querySelectorAll('input[name="price"]').forEach(radio => {
        radio.addEventListener('change', applyFilters);
    });
    
    // Clear filters button
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
}

function applyFilters() {
    filteredProducts = allProducts.filter(product => {
        // Style filter
        const selectedStyles = Array.from(document.querySelectorAll('input[name="style"]:checked'))
            .map(el => el.value);
        if (selectedStyles.length > 0 && !selectedStyles.includes(product.style)) {
            return false;
        }
        
        // Color filter
        const selectedColors = Array.from(document.querySelectorAll('input[name="color"]:checked'))
            .map(el => el.value);
        if (selectedColors.length > 0 && !selectedColors.includes(product.color)) {
            return false;
        }
        
        // Price filter
        const selectedPrice = document.querySelector('input[name="price"]:checked').value;
        if (selectedPrice !== 'all') {
            const [min, max] = selectedPrice.split('-').map(v => v === '+' ? Infinity : parseInt(v));
            if (product.price < min || product.price > max) {
                return false;
            }
        }
        
        return true;
    });
    
    applySorting();
}

function clearFilters() {
    document.querySelectorAll('input[name="style"]').forEach(el => el.checked = false);
    document.querySelectorAll('input[name="color"]').forEach(el => el.checked = false);
    document.querySelector('input[name="price"][value="all"]').checked = true;
    applyFilters();
}

function setupSort() {
    document.getElementById('sort-select').addEventListener('change', applySorting);
}

function applySorting() {
    const sortBy = document.getElementById('sort-select').value;
    
    const sorted = [...filteredProducts].sort((a, b) => {
        switch (sortBy) {
            case 'price-low':
                return a.price - b.price;
            case 'price-high':
                return b.price - a.price;
            case 'name':
                return a.name.localeCompare(b.name);
            case 'newest':
            default:
                return b.id - a.id; // Assuming higher ID = newer
        }
    });
    
    displayProducts(sorted);
}
