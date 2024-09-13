from contextlib import redirect_stdout
from io import StringIO
from typing import Iterator
from unittest.mock import patch

import pytest
from django.core.management import call_command

from lunch_service.authentication.models import User, UserRole

pytestmark = [pytest.mark.unit, pytest.mark.django_db]


def test_create_company_admin_command_success() -> None:
    # Mock inputs for username, email, and password
    inputs: Iterator[str] = iter(['testuser', 'testuser@example.com', 'password123'])

    with patch('builtins.input', lambda _: next(inputs)):
        call_command('create_company_admin')

    # Check if the user was created
    user: User = User.objects.get(username='testuser')
    assert user.email == 'testuser@example.com'
    assert user.role == UserRole.ADMIN
    assert user.check_password('password123')  # Check if the password is set correctly


def test_create_company_admin_command_user_exists() -> None:
    # Create a user that already exists
    User.objects.create_user(username='existinguser', email='existinguser@example.com', password='password123')

    # Mock inputs for username, email, and password
    inputs: Iterator[str] = iter(['existinguser', 'newuser@example.com', 'password123'])
    out: StringIO = StringIO()
    with patch('builtins.input', lambda _: next(inputs)):
        with redirect_stdout(out):
            call_command('create_company_admin')

    stdout_output: str = out.getvalue()
    assert stdout_output.strip() == 'User already exists'
    # Ensure no new user is created
    assert User.objects.filter(username='existinguser').count() == 1
    assert User.objects.filter(username='newuser').count() == 0
