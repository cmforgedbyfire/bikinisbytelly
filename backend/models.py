from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    style = db.Column(db.String(100))  # triangle, halter, bandeau, etc.
    color = db.Column(db.String(100))
    material = db.Column(db.String(200))
    main_image = db.Column(db.String(500))
    images = db.Column(db.JSON)  # List of image URLs
    color_options = db.Column(db.JSON)  # Available colors
    stock_status = db.Column(db.String(50), default='available')
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'style': self.style,
            'color': self.color,
            'material': self.material,
            'main_image': self.main_image or '/static/images/placeholder.jpg',
            'images': self.images or [],
            'color_options': self.color_options or [],
            'stock_status': self.stock_status,
            'is_featured': self.is_featured
        }


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Customer info
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50))
    
    # Shipping address
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(100))
    shipping_state = db.Column(db.String(50))
    shipping_zip = db.Column(db.String(20))
    
    # Order details
    items = db.Column(db.JSON, nullable=False)  # List of order items
    subtotal = db.Column(db.Float, nullable=False)
    shipping_cost = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)
    
    # Payment
    payment_status = db.Column(db.String(50), default='pending')  # pending, paid, failed, refunded
    payment_intent_id = db.Column(db.String(200))
    
    # Status
    status = db.Column(db.String(50), default='received')  # received, processing, shipped, delivered, cancelled
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'total': self.total,
            'status': self.status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat(),
            'items': self.items
        }


class CustomOrder(db.Model):
    __tablename__ = 'custom_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Customer info
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50))
    
    # Design details
    style = db.Column(db.String(100))
    primary_color = db.Column(db.String(100))
    secondary_color = db.Column(db.String(100))
    pattern = db.Column(db.String(100))
    special_requests = db.Column(db.Text)
    
    # Measurements
    measurements = db.Column(db.JSON)  # All measurements as JSON
    
    # Budget and pricing
    budget = db.Column(db.String(50))
    quoted_price = db.Column(db.Float)
    
    # Reference images
    reference_images = db.Column(db.JSON)
    
    # Status
    status = db.Column(db.String(50), default='pending')  # pending, quoted, approved, in_progress, completed, cancelled
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'status': self.status,
            'style': self.style,
            'created_at': self.created_at.isoformat()
        }


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    review = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False)  # Admin approval
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'name': self.name,
            'rating': self.rating,
            'review': self.review,
            'created_at': self.created_at.isoformat()
        }


class Newsletter(db.Model):
    __tablename__ = 'newsletter'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    subscribed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    responded = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
