import datetime
from typing import List

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from lunch_service.authentication.models import User, UserRole
from lunch_service.employee.models import Vote
from lunch_service.restaurant.models import Menu, Restaurant
from lunch_service.restaurant.serializers import MenuWithRestaurantSerializer


@pytest.mark.django_db
def test_top_voted_menu_view(api_client: APIClient, restaurant: Restaurant) -> None:
    menus: List[Menu] = baker.make(Menu, restaurant=restaurant, date=datetime.date.today(), _quantity=5)
    employees: List[User] = baker.make(User, role=UserRole.EMPLOYEE, _quantity=5)

    Vote.objects.create(employee=employees[0], menu=menus[0], points=Vote.Points.Top, date=datetime.date.today())
    Vote.objects.create(employee=employees[1], menu=menus[1], points=Vote.Points.Second, date=datetime.date.today())

    url: str = reverse('top-voted-menu')
    response = api_client.get(url)

    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'success'

    # Deserialize the top menu data to compare
    top_menu_data: dict = MenuWithRestaurantSerializer(menus[0]).data  # Assuming menus[0] is the top voted
    assert response.data['menu'] == top_menu_data, "The top voted menu returned does not match the expected menu"

    Vote.objects.create(employee=employees[0], menu=menus[1], points=Vote.Points.Second, date=datetime.date.today())
    response = api_client.get(url)

    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data['menu']['id'] == menus[1].pk
