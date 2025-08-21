#!/usr/bin/env python3
"""
Healytics Dependency Installation Script
This script installs dependencies step by step to avoid compatibility issues.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Healytics Dependency Installation")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found. Please run setup.py first.")
        return
    
    # Upgrade pip first
    if not run_command("venv\\Scripts\\python.exe -m pip install --upgrade pip", "Upgrading pip"):
        return
    
    # Install packages one by one to avoid conflicts
    packages = [
        ("Django==4.2.7", "Django"),
        ("djangorestframework==3.14.0", "Django REST Framework"),
        ("djangorestframework-simplejwt==5.3.0", "Django REST Framework Simple JWT"),
        ("django-cors-headers==4.3.1", "Django CORS Headers"),
        ("Pillow==10.1.0", "Pillow"),
        ("numpy==1.26.0", "NumPy"),
        ("requests==2.31.0", "Requests"),
        ("python-decouple==3.8", "Python Decouple"),
        ("gunicorn==21.2.0", "Gunicorn"),
        ("whitenoise==6.6.0", "WhiteNoise"),
        ("opencv-python==4.8.1.78", "OpenCV Python"),
        ("tensorflow-cpu==2.15.0", "TensorFlow CPU"),
    ]
    
    for package, name in packages:
        if not run_command(f"venv\\Scripts\\pip install {package}", f"Installing {name}"):
            print(f"⚠️  Failed to install {name}, but continuing...")
    
    print("\n✅ Dependency installation completed!")
    print("\nNext steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py createsuperuser (optional)")
    print("4. Start the server: python manage.py runserver")

if __name__ == "__main__":
    main()
