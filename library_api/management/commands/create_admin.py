from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library_api.models import UserProfile

class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            # Create admin user
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            # Create admin profile
            UserProfile.objects.create(
                user=admin,
                user_type='librarian'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
