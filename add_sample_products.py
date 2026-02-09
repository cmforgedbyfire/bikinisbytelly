"""
Sample Product Creator
Run this script to add sample products to your database for testing
"""

from app import app, db
from backend.models import Product

def create_sample_products():
    """Create sample products for testing"""
    
    sample_products = [
        {
            'name': 'Ocean Blue Triangle Bikini',
            'description': 'Beautiful handcrafted triangle bikini in stunning ocean blue. Perfect for beach days and poolside lounging. Made with premium swimwear fabric.',
            'price': 89.99,
            'style': 'triangle',
            'color': 'blue',
            'material': 'Premium swimwear fabric with UV protection',
            'main_image': '/static/images/placeholder.jpg',
            'images': ['/static/images/placeholder.jpg'],
            'color_options': ['#006994', '#40E0D0', '#FFFFFF'],
            'is_featured': True
        },
        {
            'name': 'Turquoise Halter Bikini',
            'description': 'Stunning turquoise halter bikini with adjustable ties. Handcrafted with attention to detail. Provides excellent support and style.',
            'price': 94.99,
            'style': 'halter',
            'color': 'turquoise',
            'material': 'Premium swimwear fabric',
            'main_image': '/static/images/placeholder.jpg',
            'images': ['/static/images/placeholder.jpg'],
            'color_options': ['#40E0D0', '#006994'],
            'is_featured': True
        },
        {
            'name': 'Coral Bandeau Set',
            'description': 'Vibrant coral bandeau bikini set. Strapless design with removable padding. Handmade with love and premium materials.',
            'price': 79.99,
            'style': 'bandeau',
            'color': 'coral',
            'material': 'Premium swimwear fabric with elastic band',
            'main_image': '/static/images/placeholder.jpg',
            'images': ['/static/images/placeholder.jpg'],
            'color_options': ['#FF7F50', '#FFB6C1'],
            'is_featured': True
        },
        {
            'name': 'White Crochet Bikini',
            'description': 'Elegant white crochet bikini, handcrafted with intricate detail. Perfect for a bohemian beach look. Fully lined for comfort.',
            'price': 109.99,
            'style': 'triangle',
            'color': 'white',
            'material': 'Premium crochet cotton with lining',
            'main_image': '/static/images/placeholder.jpg',
            'images': ['/static/images/placeholder.jpg'],
            'color_options': ['#FFFFFF', '#F5E6D3'],
            'is_featured': True
        },
        {
            'name': 'High Waist Blue Set',
            'description': 'Retro-inspired high waist bikini set in ocean blue. Flattering fit with full coverage. Handmade with premium fabric.',
            'price': 99.99,
            'style': 'high-waist',
            'color': 'blue',
            'material': 'Premium swimwear fabric',
            'main_image': '/static/images/placeholder.jpg',
            'images': ['/static/images/placeholder.jpg'],
            'color_options': ['#006994', '#40E0D0'],
            'is_featured': False
        },
        {
            'name': 'Aqua One Piece',
            'description': 'Stunning aqua one-piece swimsuit with elegant cut-outs. Handcrafted for the perfect fit. Sophisticated and stylish.',
            'price': 119.99,
            'style': 'one-piece',
            'color': 'turquoise',
            'material': 'Premium swimwear fabric with power mesh',
            'main_image': '/static/images/placeholder.jpg',
            'images': ['/static/images/placeholder.jpg'],
            'color_options': ['#40E0D0', '#006994'],
            'is_featured': True
        }
    ]
    
    with app.app_context():
        # Clear existing products (optional - comment out if you want to keep existing)
        # Product.query.delete()
        
        # Add sample products
        for product_data in sample_products:
            product = Product(**product_data)
            db.session.add(product)
            print(f"✓ Added: {product.name}")
        
        db.session.commit()
        print(f"\n✅ Successfully added {len(sample_products)} sample products!")
        print("Visit http://localhost:5000/products to see them")

if __name__ == '__main__':
    print("Creating sample products...")
    print("-" * 50)
    create_sample_products()
