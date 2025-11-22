import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vet_clinic.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Create Groups
Group.objects.get_or_create(name='Veterinario')
Group.objects.get_or_create(name='Recepcionista')

# Create Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' created.")
else:
    print("Superuser 'admin' already exists.")
