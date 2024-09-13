from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'CompanyAdmin'
    EMPLOYEE = 'employee', 'Employee'


class User(AbstractUser):

    role: models.CharField = models.CharField(
        max_length=10,
        choices=UserRole.choices,
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()} ({self.pk})"
