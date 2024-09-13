import datetime
from typing import List

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from lunch_service.authentication.models import User
from lunch_service.employee.models import Vote
from lunch_service.restaurant.models import Menu

pytestmark = [pytest.mark.integration, pytest.mark.django_db]


@pytest.fixture
def menus() -> List[Menu]:
    today: datetime.date = datetime.date.today()
    return baker.make(Menu, date=today, _quantity=4)


@pytest.mark.django_db
def test_complex_voting_scenario_with_overrides(employee_client: APIClient, employee: User, menus: List[Menu]) -> None:
    vote_url: str = reverse('vote_menu')
    # Initial vote using the old API version
    response = employee_client.post(vote_url, {'menu': menus[0].id}, format='json')
    assert response.status_code == 201
    assert Vote.objects.filter(employee=employee, menu=menus[0]).exists()

    # Override the initial vote with a new vote using the old API version
    response = employee_client.post(vote_url, {'menu': menus[1].id}, format='json')
    assert response.status_code == 201

    assert Vote.objects.filter(employee=employee, menu=menus[0]).count() == 0
    assert Vote.objects.filter(employee=employee, menu=menus[1]).count() == 1

    # Vote using the new API version
    menu_ids: List[int] = [menu.id for menu in menus[:3]]
    response = employee_client.post(vote_url, {'menus': menu_ids}, format='json', HTTP_X_API_VERSION='2.0')
    assert response.status_code == 201
    assert Vote.objects.filter(employee=employee).count() == 3

    # Attempt to vote again using the new API version to override previous votes
    reversed_menu_ids: List[int] = list(reversed(menu_ids))
    response = employee_client.post(vote_url, {'menus': reversed_menu_ids}, format='json', HTTP_X_API_VERSION='2.0')
    assert response.status_code == 201

    assert Vote.objects.filter(employee=employee).count() == 3
    for i, menu_id in enumerate(reversed_menu_ids, start=1):
        vote: Vote = Vote.objects.get(employee=employee, menu_id=menu_id)
        expected_points: int = Vote.Points.Top if i == 1 else Vote.Points.Second if i == 2 else Vote.Points.Third
        assert vote.points == expected_points, f"Menu ID: {menu_id} should have {expected_points} points"
