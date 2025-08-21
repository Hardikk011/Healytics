#!/usr/bin/env python3
"""
Setup script for Healytics Cancer Health Prediction System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Error: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("Error: Node.js is not installed. Please install Node.js 16 or higher")
    return False

def setup_backend():
    """Setup Django backend"""
    print("\n🔧 Setting up Django backend...")
    
    # Create virtual environment
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        if not run_command('python -m venv venv'):
            return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = 'venv\\Scripts\\pip'
        python_cmd = 'venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        pip_cmd = 'venv/bin/pip'
        python_cmd = 'venv/bin/python'
    
    print("Installing Python dependencies...")
    if not run_command(f'{pip_cmd} install -r requirements.txt'):
        return False
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Check if model file exists
    model_path = Path('models/skin_disease_model_best.h5')
    if not model_path.exists():
        print("⚠️  Warning: skin_disease_model_best.h5 not found in models/ directory")
        print("   Please place your model file in the models/ directory")
    
    # Run migrations
    print("Running database migrations...")
    if not run_command(f'{python_cmd} manage.py makemigrations'):
        return False
    if not run_command(f'{python_cmd} manage.py migrate'):
        return False
    
    print("✓ Django backend setup completed")
    return True

def setup_frontend():
    """Setup React frontend"""
    print("\n🔧 Setting up React frontend...")
    
    # Check if frontend directory exists
    if not os.path.exists('frontend'):
        print("Error: frontend directory not found")
        return False
    
    # Install npm dependencies
    print("Installing Node.js dependencies...")
    if not run_command('npm install', cwd='frontend'):
        return False
    
    print("✓ React frontend setup completed")
    return True

def create_superuser():
    """Create Django superuser"""
    print("\n👤 Creating Django superuser...")
    print("Please enter the following details for the admin user:")
    
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not username or not email or not password:
        print("All fields are required")
        return False
    
    # Create superuser using Django management command
    if os.name == 'nt':  # Windows
        python_cmd = 'venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        python_cmd = 'venv/bin/python'
    
    # Use subprocess with input for interactive command
    try:
        process = subprocess.Popen(
            [python_cmd, 'manage.py', 'createsuperuser', '--noinput'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send input to the process
        input_data = f"{username}\n{email}\n{password}\n{password}\n"
        stdout, stderr = process.communicate(input=input_data)
        
        if process.returncode == 0:
            print("✓ Superuser created successfully")
            return True
        else:
            print(f"Error creating superuser: {stderr}")
            return False
    except Exception as e:
        print(f"Error creating superuser: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Healytics Cancer Health Prediction System Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        return False
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        return False
    
    # Ask if user wants to create superuser
    create_admin = input("\nDo you want to create a Django admin user? (y/n): ").strip().lower()
    if create_admin in ['y', 'yes']:
        if not create_superuser():
            print("❌ Superuser creation failed")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Place your skin_disease_model_best.h5 file in the models/ directory")
    print("2. Start the Django server: python manage.py runserver")
    print("3. Start the React server: cd frontend && npm start")
    print("4. Visit http://localhost:3000 to access the application")
    print("\n📚 For more information, see the README.md file")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
