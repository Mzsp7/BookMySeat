import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
django.setup()

from django.contrib.auth.models import User

def setup_audit_accounts():
    # 1. mzsp_ / pass@123
    if not User.objects.filter(username='mzsp_').exists():
        User.objects.create_user(username='mzsp_', password='pass@123')
        print("Created User: mzsp_")
    else:
        user = User.objects.get(username='mzsp_')
        user.set_password('pass@123')
        user.save()
        print("Updated User: mzsp_")

    # 2. admin1 / admin@123
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser(username='admin1', email='admin@example.com', password='admin@123')
        print("Created Admin: admin1")
    else:
        user = User.objects.get(username='admin1')
        user.is_staff = True
        user.is_superuser = True
        user.set_password('admin@123')
        user.save()
        print("Updated Admin: admin1")

if __name__ == '__main__':
    setup_audit_accounts()
