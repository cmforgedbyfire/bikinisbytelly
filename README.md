# Bikinis By Telly - E-Commerce Website

A complete, platinum-level e-commerce website for handmade bikini sales with comprehensive business management features.

## 🌊 Features

### Customer-Facing
- **Product Gallery** with filtering and sorting
- **Custom Order System** for personalized bikinis
- **Shopping Cart** with local storage
- **Secure Checkout** with Stripe integration
- **Size Guide** and measurement calculator
- **Customer Reviews** (submission and moderation)
- **Newsletter Signup**
- **Responsive Design** (mobile, tablet, desktop)

### Business Management
- **Order Management** (tracking, status updates)
- **Inventory Tracking**
- **Customer Database**
- **Email Automation** (confirmations, shipping notifications)
- **Receipt & Invoice Generation** (PDF)
- **Payment Processing** (Stripe)
- **Analytics Dashboard**
- **Review Moderation**

## 🎨 Design

**Color Scheme:**
- Ocean Blue (#006994)
- Aqua/Turquoise (#40E0D0)
- Coral Accent (#FF7F50)
- Soft Sand (#F5E6D3)
- White (#FFFFFF)

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone or Download** this project to your local machine

2. **Install Dependencies:**
```powershell
cd "f:\her company\website"
pip install -r requirements.txt
```

3. **Configure Environment:**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your actual credentials:
```powershell
copy .env.example .env
notepad .env
```

Required configuration:
- `SECRET_KEY`: Generate a random secret key
- `MAIL_PASSWORD`: Your Outlook/email password
- `STRIPE_PUBLIC_KEY`: From Stripe dashboard
- `STRIPE_SECRET_KEY`: From Stripe dashboard
- `ADMIN_PASSWORD`: Choose a secure admin password

4. **Initialize Database:**
```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

5. **Run the Application:**
```powershell
python app.py
```

6. **Access the Website:**
   - Website: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin (coming soon)

## 📧 Email Configuration

The site uses Outlook/Hotmail for sending emails.

**Email Address:** bikinisbytelly@outlook.com

To enable email functionality:
1. Go to your Outlook account settings
2. Enable "Two-Step Verification"
3. Generate an "App Password"
4. Use the app password in your `.env` file

## 💳 Payment Configuration

1. **Create Stripe Account:**
   - Go to https://stripe.com
   - Sign up for an account
   - Get your API keys from the dashboard

2. **Configure Stripe:**
   - Add keys to `.env` file
   - For testing, use Stripe test mode
   - Test card: `4242 4242 4242 4242`

3. **Webhook Setup (for production):**
   - In Stripe dashboard, add webhook endpoint
   - URL: `https://yourdomain.com/webhook/stripe`
   - Events: `payment_intent.succeeded`

## 🗂️ Project Structure

```
website/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── static/
│   ├── css/
│   │   ├── style.css      # Main stylesheet
│   │   └── additional.css # Extended styles
│   ├── js/
│   │   ├── main.js        # Core JavaScript
│   │   ├── products.js    # Product listing
│   │   ├── cart.js        # Shopping cart
│   │   ├── checkout.js    # Checkout process
│   │   └── custom-order.js
│   └── images/            # Product images
├── templates/             # HTML templates
├── backend/
│   ├── models.py         # Database models
│   ├── email_service.py  # Email automation
│   ├── payment_service.py # Stripe integration
│   └── receipt_generator.py # PDF generation
├── database/             # SQLite database
├── receipts/             # Generated receipts
└── invoices/             # Generated invoices
```

## 🚀 Usage

### Adding Products

Products can be added via the admin panel or directly in the database:

```python
from app import app, db
from backend.models import Product

with app.app_context():
    product = Product(
        name="Ocean Blue Triangle Bikini",
        description="Handcrafted triangle bikini in beautiful ocean blue",
        price=89.99,
        style="triangle",
        color="blue",
        material="Premium swimwear fabric",
        main_image="/static/images/product1.jpg",
        is_featured=True
    )
    db.session.add(product)
    db.session.commit()
```

### Managing Orders

Orders are automatically created when customers checkout. View them in the admin panel or query the database:

```python
from backend.models import Order

# Get all orders
orders = Order.query.all()

# Get specific order
order = Order.query.filter_by(order_number='ORD-20260209-ABC123').first()
```

### Sending Emails

Emails are sent automatically for:
- Order confirmations
- Custom order requests
- Shipping notifications
- Contact form submissions
- Newsletter signups

## 🔧 Customization

### Changing Colors

Edit `static/css/style.css` and update the CSS variables:

```css
:root {
    --primary-blue: #006994;
    --secondary-aqua: #40E0D0;
    --accent-coral: #FF7F50;
    /* ... etc */
}
```

### Adding Pages

1. Create HTML template in `templates/`
2. Add route in `app.py`:

```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

3. Add navigation link in `templates/base.html`

## 📊 Admin Features (Coming Soon)

The admin dashboard will include:
- Order management and status updates
- Product inventory management
- Customer database
- Sales analytics
- Review moderation
- Email campaign management

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use strong passwords for admin account
- Keep Stripe secret key confidential
- Use HTTPS in production
- Regularly update dependencies

## 🐛 Troubleshooting

**Database errors:**
```powershell
# Reset database
rm database\bikinis_by_telly.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**Email not sending:**
- Verify Outlook app password is correct
- Check Outlook account isn't locked
- Ensure two-step verification is enabled

**Stripe errors:**
- Verify API keys are correct
- Check if using test vs. production keys
- Review Stripe dashboard for error details

## 📝 License

MIT License - Free to use and modify

## 💬 Support

For questions or support:
- Email: bikinisbytelly@outlook.com

## 🎯 Future Enhancements

- Full admin dashboard
- Product image upload interface
- Instagram feed integration
- Social media sharing
- Customer accounts/login
- Wishlist functionality
- Gift cards
- Discount codes
- Advanced analytics

---

**Built with love for Telly's Bikini Business** 🌊👙

Made with Flask, Stripe, and premium design principles.
