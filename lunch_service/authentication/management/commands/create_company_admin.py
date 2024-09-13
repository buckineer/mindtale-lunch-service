# Assuming this file is located at your_django_project/your_app/management/commands/create_superadmin.py

from typing import Any, Optional

from django.core.management.base import BaseCommand

from lunch_service.authentication.models import User, UserRole


class Command(BaseCommand):
    help: str = 'Create a company admin user'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        username: str = input('Enter username: ')
        email: str = input('Enter email: ')
        password: str = input('Enter password: ')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('User already exists'))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role=UserRole.ADMIN
            )
            self.stdout.write(self.style.SUCCESS('Company Admin created successfully'))
        return None
