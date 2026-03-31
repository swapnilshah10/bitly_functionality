from django.contrib.auth.models import User

# Try to find an existing superuser
superuser = User.objects.filter(is_superuser=True).first()

if superuser:
    superuser.set_password('admin123!')
    superuser.save()
    print(f"SUCCESS: Reset password for existing superuser: {superuser.username}")
else:
    print("No superuser found. Creating a new one...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123!')
    print("SUCCESS: Created new superuser: admin")
