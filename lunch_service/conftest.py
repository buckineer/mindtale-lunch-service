import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from lunch_service.authentication.models import User, UserRole
from lunch_service.restaurant.models import Menu, Restaurant


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def company_admin_user() -> User:
    return baker.make(User, username='admin', password='password', role=UserRole.ADMIN)


@pytest.fixture
def employee() -> User:
    return baker.make(User, username='employee', password='password', role=UserRole.EMPLOYEE)


@pytest.fixture
def company_authenticated_client(api_client: APIClient, company_admin_user: User) -> APIClient:
    api_client.force_authenticate(user=company_admin_user)
    return api_client


@pytest.fixture
def restaurant() -> Restaurant:
    return baker.make(Restaurant, name='Test Restaurant', api_key='test_api_key')


@pytest.fixture
def authenticated_restaurant_client(api_client: APIClient, restaurant: Restaurant) -> APIClient:
    api_client.credentials(HTTP_API_KEY=restaurant.api_key)
    return api_client


@pytest.fixture
def menu_today():
    import datetime
    return baker.make(Menu, date=datetime.datetime.today())


@pytest.fixture
def employee_client(api_client, employee):
    api_client.force_authenticate(user=employee)
    return api_client
