import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from lunch_service.authentication.models import User, UserRole
from lunch_service.employee.models import Menu, Vote

pytestmark = [pytest.mark.integration, pytest.mark.django_db]


def test_admin_can_create_employee(company_authenticated_client: APIClient) -> None:
    url: str = reverse('create_employee')
    data: dict = {
        'username': 'new_employee',
        'password': 'password123',
        "retype_password": "password123"
    }
    response = company_authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='new_employee', role=UserRole.EMPLOYEE).exists()
    assert User.objects.filter(username='new_employee', role=UserRole.EMPLOYEE).first().check_password(data['password'])  # type: ignore


def test_non_admin_cannot_create_employee(employee_client: APIClient, api_client: APIClient) -> None:
    url: str = reverse('create_employee')
    data: dict = {
        'username': 'another_employee',
        'password': 'password123',
    }
    response = employee_client.post(url, data)
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]


def test_employee_can_vote(employee_client: APIClient, menu_today: Menu, employee: User) -> None:
    url: str = reverse('vote_menu')
    data: dict = {'menu': menu_today.id}
    response = employee_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.filter(employee=employee, menu=menu_today).exists()


def test_non_employee_cannot_vote(company_authenticated_client: APIClient, menu_today: Menu) -> None:
    url: str = reverse('vote_menu')
    data: dict = {'menu': menu_today.id}
    response = company_authenticated_client.post(url, data, format='json')
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]


def test_employee_can_vote_with_new_api(employee_client: APIClient, menu_today: Menu, employee: User) -> None:
    url: str = reverse('vote_menu')
    data: dict = {'menus': [menu_today.id]}
    response = employee_client.post(url, data, format='json', HTTP_X_API_VERSION='2.0')
    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.filter(employee=employee, menu=menu_today).exists()
