// Custom Order Form

document.addEventListener('DOMContentLoaded', () => {
    setupCustomOrderForm();
});

function setupCustomOrderForm() {
    const form = document.getElementById('custom-order-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validate measurements
        const requiredMeasurements = ['bust', 'under_bust', 'waist', 'hips'];
        for (const field of requiredMeasurements) {
            if (!data[field] || parseFloat(data[field]) <= 0) {
                showAlert(`Please provide a valid ${field.replace('_', ' ')} measurement`, 'error');
                return;
            }
        }
        
        // Handle file uploads
        const fileInput = document.getElementById('reference-images');
        const files = fileInput.files;
        
        // Create FormData for file upload
        const uploadData = new FormData();
        for (let key in data) {
            uploadData.append(key, data[key]);
        }
        
        for (let i = 0; i < files.length; i++) {
            uploadData.append('images', files[i]);
        }
        
        try {
            const response = await fetch('/api/custom-order', {
                method: 'POST',
                body: uploadData
            });
            
            if (response.ok) {
                const result = await response.json();
                showAlert('Custom order request submitted! We\'ll contact you within 24 hours.', 'success');
                
                // Redirect to confirmation page
                setTimeout(() => {
                    window.location.href = `/custom-order-confirmation/${result.order_id}`;
                }, 2000);
            } else {
                const error = await response.json();
                showAlert(error.message || 'Failed to submit order. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error submitting custom order:', error);
            showAlert('Error submitting order. Please email us at bikinisbytelly@outlook.com', 'error');
        }
    });
    
    // Add real-time validation for measurements
    const measurementInputs = document.querySelectorAll('input[type="number"]');
    measurementInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && parseFloat(this.value) <= 0) {
                this.style.borderColor = 'var(--error)';
                showAlert('Measurement must be greater than 0', 'error');
            } else {
                this.style.borderColor = '';
            }
        });
    });
}
