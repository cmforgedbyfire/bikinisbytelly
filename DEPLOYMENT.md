# Bikinis By Telly - Deployment Guide

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Railway (RECOMMENDED) ⭐
**Best for:** Flask apps with database and Stripe
**Free Tier:** Yes (with limits)
**Setup Time:** 5 minutes

#### Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select bikinisbytelly repository
5. Railway auto-detects Flask
6. Add environment variables in Railway dashboard
7. Deploy! 🎉

**Custom Domain:**
- Settings → Domains → Add bikinisbytelly.com
- Update DNS records as shown

---

### Option 2: Render
**Best for:** Python apps, great free tier
**Free Tier:** Yes
**Setup Time:** 5-10 minutes

#### Steps:
1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Connect bikinisbytelly repository
5. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
6. Add environment variables
7. Deploy!

**Custom Domain:**
- Settings → Custom Domain → bikinisbytelly.com

---

### Option 3: Heroku
**Classic choice, very reliable**
**Free Tier:** Limited
**Setup Time:** 10 minutes

#### Steps:
1. Install Heroku CLI
2. `heroku create bikinisbytelly`
3. `heroku config:set KEY=value` (for each .env variable)
4. `git push heroku main`
5. `heroku domains:add bikinisbytelly.com`

---

### Option 4: PythonAnywhere
**Best for:** Simple deployment, good for beginners
**Free Tier:** Yes (with ads)
**Setup Time:** 15 minutes

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Required Files (Already Created ✓)
- [x] requirements.txt
- [x] .gitignore
- [x] .env.example
- [x] Procfile (need to create)
- [x] runtime.txt (optional)

### Environment Variables to Set
Copy these from your .env to hosting platform:
```
SECRET_KEY=
DATABASE_URL= (will be provided by host)
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=bikinisbytelly@outlook.com
MAIL_PASSWORD=
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
BUSINESS_EMAIL=bikinisbytelly@outlook.com
BUSINESS_NAME=Bikinis By Telly
ADMIN_USERNAME=admin
ADMIN_PASSWORD=
```

### DNS Configuration
Point bikinisbytelly.com to your hosting:

**For Railway/Render:**
- Add CNAME record
- Host: www
- Value: (provided by hosting)
- Add A record for root domain

**TTL:** 3600 (or auto)

---

## 🔧 DEPLOYMENT FILES NEEDED

### Procfile
```
web: gunicorn app:app
```

### runtime.txt (optional)
```
python-3.11.0
```

### Additional Dependencies
Add to requirements.txt:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9  # For PostgreSQL (Railway/Render)
```

---

## 🎯 RECOMMENDED DEPLOYMENT STEPS

1. **Prepare Repository**
   - Commit all files
   - Push to GitHub
   
2. **Choose Railway (Easiest)**
   - Connect GitHub repo
   - Auto-deploys on push
   - Built-in database
   - Easy environment variables
   
3. **Configure Domain**
   - Add bikinisbytelly.com in Railway
   - Update DNS records
   - SSL auto-configured
   
4. **Test Everything**
   - Test order flow
   - Test payment (use test mode first)
   - Test emails
   
5. **Go Live!**
   - Switch Stripe to live mode
   - Update STRIPE_SECRET_KEY
   - Announce launch! 🎉

---

## 🔒 SECURITY FOR PRODUCTION

- [x] .env not in git (in .gitignore)
- [ ] Change ADMIN_PASSWORD to strong password
- [ ] Use production Stripe keys (not test)
- [ ] Set SECRET_KEY to random value
- [ ] Enable HTTPS (auto on Railway/Render)
- [ ] Set up Stripe webhooks for production URL

---

## 📞 NEED HELP?

**Quick Deploy with Railway:**
1. Push code to GitHub
2. Import to Railway
3. Add environment variables
4. Deploy!
5. Connect domain
6. Done in 5 minutes! ✅

The site will be live at bikinisbytelly.com! 🌊
