import json
from typing import Any, Dict, List

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from lunch_service.restaurant.models import Menu, Restaurant

pytestmark = [pytest.mark.integration, pytest.mark.django_db]


def test_create_restaurant(company_authenticated_client: APIClient) -> None:
    restaurant: Restaurant = baker.prepare(Restaurant)
    data: Dict[str, Any] = {
        'name': restaurant.name
    }
    url: str = reverse('create_restaurant')
    response = company_authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    ret_data: Dict[str, Any] = response.json()
    assert Restaurant.objects.count() == 1
    assert Restaurant.objects.get(pk=ret_data['id']).name == restaurant.name


def test_create_menu(authenticated_restaurant_client: APIClient, restaurant: Restaurant) -> None:
    url: str = reverse('create_menu')
    items: List[Dict[str, Any]] = [
        {'name': 'Pizza', 'price': 10},
        {'name': 'Burger', 'price': 8}
    ]
    data: Dict[str, Any] = {
        'date': '2024-09-12',
        'items': json.dumps(items)  # Convert list to JSON string
    }
    response = authenticated_restaurant_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    assert Menu.objects.count() == 1
    menu: Menu = Menu.objects.get()
    assert menu.restaurant == restaurant
    assert json.loads(menu.items)[0]['name'] == 'Pizza'
    assert json.loads(menu.items)[1]['name'] == 'Burger'


def test_create_restaurant_unauthorized(api_client: APIClient) -> None:
    url: str = reverse('create_restaurant')
    data: Dict[str, Any] = {
        'name': 'Unauthorized Restaurant'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_menu_unauthorized(api_client: APIClient) -> None:
    url: str = reverse('create_menu')
    items: List[Dict[str, Any]] = [
        {'name': 'Pizza', 'price': 10},
        {'name': 'Burger', 'price': 8}
    ]
    data: Dict[str, Any] = {
        'date': '2024-09-12',
        'items': json.dumps(items)  # Convert list to JSON string
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
