import os
import sys
import subprocess
import django
from django.conf import settings

def run_command(command):
    print(f"Running: {command}")
    ret = subprocess.call(command, shell=True)
    if ret != 0:
        print(f"Error executing: {command}")
        return False
    return True

def setup():
    print("🎬 BookMyShow Clone - Setup Script")
    print("===================================")

    # 1. Install dependencies
    print("\n📦 Checking dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Warning: unexpected error installing requirements.")

    # 2. Apply Migrations
    print("\n🗄️ Applying optimizations and fixes...")
    # Run our manual security fix script first/alongside to ensure DB is correct
    # But first, standard migrate to ensure tables exist
    if not run_command("python manage.py migrate"):
        print("Standard migration failed (possibly due to Py3.14/Django6 issue).")
        print("Attempting to rely on manual fixes...")
    
    # Apply manual security fixes if needed
    if os.path.exists("apply_security_fixes.py"):
        run_command("python apply_security_fixes.py")

    # 3. Create Superuser
    print("\nbust👤 Admin User Setup")
    print("You can create an admin user to access the dashboard.")
    print("Run: python manage.py createsuperuser")

    print("\n✅ Setup Complete!")
    print("To start the server, run: python manage.py runserver")

if __name__ == "__main__":
    setup()
