#!/usr/bin/env python
"""
Together Culture 2.0 - Application Management Script
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main application management function"""
    print("🚀 Together Culture 2.0 - Application Manager")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        return
    
    while True:
        print("\n📋 Available Commands:")
        print("1. 🏃‍♂️  Run Development Server")
        print("2. 🧪  Run Tests")
        print("3. 📊  Run Tests with Coverage")
        print("4. 🗄️  Make Migrations")
        print("5. 🔄  Migrate Database")
        print("6. 🧹  Clean Cache Files")
        print("7. 🚪  Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n🏃‍♂️ Starting development server...")
            print("🌐 Server will be available at: http://127.0.0.1:8000")
            print("⏹️  Press Ctrl+C to stop the server")
            os.system("python manage.py runserver")
            
        elif choice == "2":
            run_command("python manage.py test", "Running tests")
            
        elif choice == "3":
            run_command("coverage run --source='.' manage.py test", "Running tests with coverage")
            run_command("coverage report", "Generating coverage report")
            
        elif choice == "4":
            run_command("python manage.py makemigrations", "Making migrations")
            
        elif choice == "5":
            run_command("python manage.py migrate", "Running migrations")
            
        elif choice == "6":
            print("\n🧹 Cleaning cache files...")
            # Remove __pycache__ directories
            for root, dirs, files in os.walk("."):
                for dir_name in dirs:
                    if dir_name == "__pycache__":
                        cache_path = os.path.join(root, dir_name)
                        try:
                            import shutil
                            shutil.rmtree(cache_path)
                            print(f"✅ Removed: {cache_path}")
                        except Exception as e:
                            print(f"❌ Failed to remove {cache_path}: {e}")
            print("✅ Cache cleaning completed!")
            
        elif choice == "7":
            print("\n👋 Goodbye! Thanks for using Together Culture 2.0!")
            break
            
        else:
            print("❌ Invalid choice. Please enter a number between 1-7.")

if __name__ == "__main__":
    main() 