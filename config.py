import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database/bikinis_by_telly.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp-mail.outlook.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'bikinisbytelly@outlook.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('BUSINESS_EMAIL', 'bikinisbytelly@outlook.com')
    
    # Stripe
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    
    # Business
    BUSINESS_EMAIL = os.getenv('BUSINESS_EMAIL', 'bikinisbytelly@outlook.com')
    BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'Bikinis By Telly')
    BUSINESS_PHONE = os.getenv('BUSINESS_PHONE', '')
    BUSINESS_ADDRESS = os.getenv('BUSINESS_ADDRESS', '')
    
    # Upload folders
    UPLOAD_FOLDER = 'static/images/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Admin
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change-this-password')
