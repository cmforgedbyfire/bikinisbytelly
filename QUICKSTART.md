# Quick Start Guide - Bikinis By Telly Website

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Python Packages
```powershell
cd "f:\her company\website"
pip install -r requirements.txt
```

### Step 2: Configure Your Settings

Create `.env` file from template:
```powershell
copy .env.example .env
```

Edit `.env` with your details:
- Change `ADMIN_PASSWORD` to a secure password
- Add your email password (see Email Setup below)
- Add Stripe keys (see Payment Setup below)

### Step 3: Initialize Database
```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Step 4: Run the Website
```powershell
python app.py
```

Visit: http://localhost:5000

## 📧 Email Setup (Required for Order Confirmations)

1. **Enable App Password in Outlook:**
   - Go to https://account.microsoft.com/security
   - Enable "Two-step verification"
   - Go to "App passwords"
   - Create new app password for "Mail"
   - Copy the generated password

2. **Add to .env file:**
```
MAIL_PASSWORD=your-app-password-here
```

## 💳 Payment Setup (Stripe)

1. **Get Stripe Account:**
   - Sign up at https://stripe.com
   - Complete account setup

2. **Get API Keys:**
   - Dashboard → Developers → API keys
   - Copy "Publishable key" and "Secret key"

3. **Add to .env:**
```
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

4. **Test Card:**
   - Card: 4242 4242 4242 4242
   - Expiry: Any future date
   - CVC: Any 3 digits

## 📦 Adding Your First Product

```python
python
>>> from app import app, db
>>> from backend.models import Product
>>> with app.app_context():
...     product = Product(
...         name="Ocean Blue Bikini",
...         description="Beautiful handmade bikini",
...         price=89.99,
...         style="triangle",
...         color="blue",
...         is_featured=True
...     )
...     db.session.add(product)
...     db.session.commit()
...     print(f"Product added! ID: {product.id}")
```

## 🎯 Key Features to Test

1. **Browse Products:** http://localhost:5000/products
2. **Custom Order:** http://localhost:5000/custom-order
3. **Shopping Cart:** Add items and checkout
4. **Contact Form:** http://localhost:5000/contact

## ⚙️ Common Commands

**Start server:**
```powershell
python app.py
```

**Reset database:**
```powershell
rm database\bikinis_by_telly.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**Check for errors:**
- Look at terminal output while server is running
- Check browser console (F12)

## 📱 Contact Email

All emails sent to/from: **bikinisbytelly@outlook.com**

Make sure this email account is set up and the password is in `.env`!

## 🎨 Customizing

- **Colors:** Edit `static/css/style.css`
- **Text:** Edit HTML files in `templates/`
- **Images:** Add to `static/images/`

## 🆘 Quick Fixes

**"Module not found" error:**
```powershell
pip install -r requirements.txt
```

**"Database is locked":**
- Close all Python processes
- Restart the server

**Emails not sending:**
- Verify email password in `.env`
- Check Outlook app password is active

**Payment not working:**
- Use test card: 4242 4242 4242 4242
- Check Stripe keys in `.env`

## 📞 Need Help?

Email: bikinisbytelly@outlook.com

---

**You're all set! Start taking orders! 🎉**
