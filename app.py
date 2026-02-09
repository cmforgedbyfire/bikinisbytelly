from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_mail import Mail, Message
from config import Config
from backend.models import db, Product, Order, CustomOrder, Review, Newsletter, Contact, Admin
from backend.email_service import EmailService
from backend.payment_service import PaymentService
from backend.receipt_generator import ReceiptGenerator
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)

# Initialize services
email_service = EmailService(app, mail)
payment_service = PaymentService(app)
receipt_generator = ReceiptGenerator(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()
    # Create default admin if doesn't exist
    admin = Admin.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
    if not admin:
        admin = Admin(username=app.config['ADMIN_USERNAME'])
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.add(admin)
        db.session.commit()

# ===== ROUTES =====

# --- PAGES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/custom-order')
def custom_order():
    return render_template('custom_order.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/size-guide')
def size_guide():
    return render_template('size_guide.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/care-instructions')
def care_instructions():
    return render_template('care_instructions.html')

@app.route('/shipping-info')
def shipping_info():
    return render_template('shipping_info.html')

@app.route('/returns')
def returns():
    return render_template('returns.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

@app.route('/custom-order-confirmation/<int:order_id>')
def custom_order_confirmation(order_id):
    order = CustomOrder.query.get_or_404(order_id)
    return render_template('custom_order_confirmation.html', order=order)

# --- API ENDPOINTS ---

@app.route('/api/products')
def api_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products/featured')
def api_featured_products():
    products = Product.query.filter_by(is_featured=True).limit(6).all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products/<int:product_id>/reviews')
def api_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id, approved=True).all()
    return jsonify([r.to_dict() for r in reviews])

@app.route('/api/reviews', methods=['POST'])
def api_submit_review():
    data = request.json
    review = Review(
        product_id=data['product_id'],
        name=data['name'],
        rating=int(data['rating']),
        review=data['review']
    )
    db.session.add(review)
    db.session.commit()
    
    # Send notification to admin
    email_service.send_new_review_notification(review)
    
    return jsonify({'success': True})

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.json
    contact = Contact(
        name=data['name'],
        email=data['email'],
        subject=data['subject'],
        message=data['message']
    )
    db.session.add(contact)
    db.session.commit()
    
    # Send confirmation to customer and notification to admin
    email_service.send_contact_confirmation(contact)
    
    return jsonify({'success': True})

@app.route('/api/newsletter/subscribe', methods=['POST'])
def api_newsletter_subscribe():
    data = request.json
    email = data['email']
    
    # Check if already subscribed
    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        if not existing.subscribed:
            existing.subscribed = True
            db.session.commit()
        return jsonify({'success': True, 'message': 'Already subscribed'})
    
    newsletter = Newsletter(email=email)
    db.session.add(newsletter)
    db.session.commit()
    
    # Send welcome email
    email_service.send_newsletter_welcome(email)
    
    return jsonify({'success': True})

@app.route('/api/custom-order', methods=['POST'])
def api_custom_order():
    data = request.form.to_dict()
    
    # Generate order number
    order_number = f"CO-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"
    
    # Handle file uploads
    uploaded_files = []
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{order_number}_{filename}")
                file.save(filepath)
                uploaded_files.append(filepath)
    
    # Create custom order
    custom_order = CustomOrder(
        order_number=order_number,
        customer_name=data['name'],
        customer_email=data['email'],
        customer_phone=data['phone'],
        style=data['style'],
        primary_color=data['primary_color'],
        secondary_color=data.get('secondary_color', ''),
        pattern=data['pattern'],
        special_requests=data.get('special_requests', ''),
        measurements={
            'bust': data['bust'],
            'under_bust': data['under_bust'],
            'waist': data['waist'],
            'hips': data['hips'],
            'additional': data.get('additional_measurements', '')
        },
        budget=data['budget'],
        reference_images=uploaded_files
    )
    
    db.session.add(custom_order)
    db.session.commit()
    
    # Send confirmation emails
    email_service.send_custom_order_confirmation(custom_order)
    
    return jsonify({'success': True, 'order_id': custom_order.id})

@app.route('/api/stripe/public-key')
def api_stripe_public_key():
    return jsonify({'publicKey': app.config['STRIPE_PUBLIC_KEY']})

@app.route('/api/create-payment-intent', methods=['POST'])
def api_create_payment_intent():
    data = request.json
    
    # Generate order number
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"
    
    # Create order
    customer = data['customer']
    order = Order(
        order_number=order_number,
        customer_name=f"{customer['first_name']} {customer['last_name']}",
        customer_email=customer['email'],
        customer_phone=customer['phone'],
        shipping_address=f"{customer['address']}\n{customer.get('address2', '')}",
        shipping_city=customer['city'],
        shipping_state=customer['state'],
        shipping_zip=customer['zip'],
        items=data['items'],
        subtotal=data['total'] / 1.08,  # Reverse calculate from total
        shipping_cost=10 if data['total'] < 100 else 0,
        tax=data['total'] * 0.08 / 1.08,
        total=data['total']
    )
    
    db.session.add(order)
    db.session.commit()
    
    # Create payment intent with Stripe
    intent = payment_service.create_payment_intent(
        amount=int(data['total'] * 100),  # Convert to cents
        order_id=order.id,
        customer_email=customer['email']
    )
    
    order.payment_intent_id = intent.id
    db.session.commit()
    
    return jsonify({
        'clientSecret': intent.client_secret,
        'orderId': order.id
    })

# Payment webhook
@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    event = payment_service.handle_webhook(payload, sig_header)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent.metadata.get('order_id')
        
        if order_id:
            order = Order.query.get(order_id)
            order.payment_status = 'paid'
            db.session.commit()
            
            # Generate receipt
            receipt_path = receipt_generator.generate_receipt(order)
            
            # Send confirmation email with receipt
            email_service.send_order_confirmation(order, receipt_path)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
