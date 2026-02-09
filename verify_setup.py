"""
Setup Verification Script
Run this to check if everything is configured correctly
"""

import os
import sys

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version OK:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("✗ Python version too old. Need 3.8+, have:", f"{version.major}.{version.minor}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_mail',
        'stripe',
        'reportlab',
        'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} NOT installed")
            missing.append(package)
    
    if missing:
        print("\nTo install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required keys"""
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  Run: copy .env.example .env")
        return False
    
    print("✓ .env file exists")
    
    # Check for critical keys
    with open('.env', 'r') as f:
        content = f.read()
        
    critical_keys = [
        'SECRET_KEY',
        'MAIL_PASSWORD',
        'STRIPE_PUBLIC_KEY',
        'STRIPE_SECRET_KEY',
        'ADMIN_PASSWORD'
    ]
    
    missing_keys = []
    for key in critical_keys:
        if f"{key}=" in content:
            value = content.split(f"{key}=")[1].split('\n')[0].strip()
            if value and value != 'your-' and value != 'change-':
                print(f"✓ {key} configured")
            else:
                print(f"⚠ {key} needs configuration")
                missing_keys.append(key)
        else:
            print(f"✗ {key} missing")
            missing_keys.append(key)
    
    return len(missing_keys) == 0

def check_folders():
    """Check if required folders exist"""
    required_folders = [
        'static',
        'static/css',
        'static/js',
        'static/images',
        'templates',
        'backend',
        'database',
        'receipts',
        'invoices'
    ]
    
    all_exist = True
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"✓ {folder}/ exists")
        else:
            print(f"✗ {folder}/ missing")
            all_exist = False
    
    return all_exist

def check_database():
    """Check if database can be initialized"""
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("BIKINIS BY TELLY - SETUP VERIFICATION")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_dependencies),
        ("Environment File", check_env_file),
        ("Folder Structure", check_folders),
        ("Database", check_database)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        print("-" * 60)
        results.append(check_func())
        print()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if all(results):
        print("✅ All checks passed! You're ready to start the website.")
        print("\nTo start the server:")
        print("  python app.py")
        print("\nOr double-click:")
        print("  START_WEBSITE.bat")
    else:
        print("⚠ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: copy .env.example .env")
        print("3. Configure .env with your credentials")
    
    print()

if __name__ == '__main__':
    main()
