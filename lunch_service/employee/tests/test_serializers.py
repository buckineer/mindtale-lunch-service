import datetime
from typing import Any, Dict, List

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.serializers import Serializer
from rest_framework.test import APIRequestFactory

from lunch_service.authentication.models import User
from lunch_service.employee.constants import ErrorMessages
from lunch_service.employee.models import Vote
from lunch_service.employee.serializers import VoteOneSerializer, VoteThreeSerializer
from lunch_service.restaurant.models import Menu

pytestmark = [pytest.mark.unit, pytest.mark.django_db]


def test_vote_one_serializer_valid(employee: User) -> None:
    menu: Menu = baker.make(Menu, date=datetime.date.today())
    url: str = reverse('vote_menu')
    request = APIRequestFactory().post(url, {'menu': menu.id})
    request.user = employee
    data: Dict[str, Any] = {'menu': menu.id}
    serializer: Serializer = VoteOneSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    assert Vote.objects.filter(employee=employee, menu=menu).exists()


def test_vote_one_serializer_invalid_date() -> None:
    menu: Menu = baker.make(Menu, date=datetime.date.today() - datetime.timedelta(days=1))
    data: Dict[str, Any] = {'menu': menu.id}
    serializer: Serializer = VoteOneSerializer(data=data)
    assert not serializer.is_valid()
    assert 'menu' in serializer.errors
    assert any(str(error) == ErrorMessages.ONLY_VOTE_FOR_MENU_OF_TODAY for error in serializer.errors['menu'])


def test_vote_three_serializer_valid(employee: User) -> None:
    menus: List[Menu] = baker.make(Menu, date=datetime.date.today(), _quantity=3)
    request = APIRequestFactory().post('/')
    request.user = employee
    data: Dict[str, Any] = {'menus': [menu.id for menu in menus]}
    serializer: Serializer = VoteThreeSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    result: Dict[str, Any] = serializer.save()
    votes: List[Vote] = result['votes']
    assert len(votes) == 3
    assert all(vote.points == Vote.Points.choices[index][0] for index, vote in enumerate(votes))
    for menu in result['menus']:
        assert Vote.objects.filter(employee=employee, menu=menu).exists()


def test_vote_three_serializer_invalid_date() -> None:
    menus: List[Menu] = baker.make(Menu, date=datetime.date.today(), _quantity=2)
    old_date_menu: Menu = baker.make(Menu, date=datetime.date.today() - datetime.timedelta(days=1))
    menus.append(old_date_menu)

    data: Dict[str, Any] = {'menus': [menu.id for menu in menus]}
    serializer: Serializer = VoteThreeSerializer(data=data)
    assert not serializer.is_valid()
    assert 'menus' in serializer.errors
    assert str(serializer.errors['menus'][0]) == ErrorMessages.ALL_VOTE_MUST_BE_FOR_TODAY_MENU


def test_vote_three_serializer_invalid_length() -> None:
    menus: List[Menu] = baker.make(Menu, date=datetime.date.today(), _quantity=5)
    data: Dict[str, Any] = {'menus': [menu.id for menu in menus]}
    serializer: Serializer = VoteThreeSerializer(data=data)
    assert not serializer.is_valid()
    assert 'menus' in serializer.errors
    assert serializer.errors['menus'][0].code == 'max_length'
