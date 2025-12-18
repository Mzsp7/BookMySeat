import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
django.setup()

User = get_user_model()

# Create standard user
if not User.objects.filter(username='tester').exists():
    User.objects.create_user('tester', 'tester@example.com', 'testpass123')
    print("Created standard user: tester")

# Create admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
    print("Created admin user: admin")
