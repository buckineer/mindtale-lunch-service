import datetime
from typing import Any, Dict, List

from django.core.exceptions import MultipleObjectsReturned
from django.db import transaction
from rest_framework import serializers

from lunch_service.authentication.models import User, UserRole

from .constants import ErrorMessages
from .models import Menu, Vote


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    retype_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'retype_password', 'email', 'first_name', 'last_name']

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if data['password'] != data['retype_password']:
            raise serializers.ValidationError({"password": "The two passwords must match."})
        return data

    def create(self, validated_data: Dict[str, Any]) -> User:
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=UserRole.EMPLOYEE
        )


class VoteOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['menu']

    def validate_menu(self, value: Menu) -> Menu:
        if value.date != datetime.date.today():
            raise serializers.ValidationError(ErrorMessages.ONLY_VOTE_FOR_MENU_OF_TODAY)
        return value

    def create(self, validated_data: Dict[str, Any]) -> Vote:
        employee = self.context['request'].user
        menu = validated_data['menu']
        today = datetime.date.today()
        try:
            vote, _ = Vote.objects.update_or_create(
                employee=employee,
                date=today,
                defaults={'menu': menu, 'points': Vote.Points.Top}
            )
        except MultipleObjectsReturned:
            Vote.objects.filter(employee=employee, date=today, points=Vote.Points.Top).delete()
            vote = Vote.objects.create(employee=employee, date=today, menu=menu)
        return vote


class VoteThreeSerializer(serializers.Serializer):
    menus = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all()),
        min_length=1,
        max_length=3
    )

    def validate_menus(self, menus: List[Menu]) -> List[Menu]:
        today = datetime.date.today()
        if any(menu.date != today for menu in menus):
            raise serializers.ValidationError(ErrorMessages.ALL_VOTE_MUST_BE_FOR_TODAY_MENU)
        return menus

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        employee = self.context['request'].user
        menus = validated_data['menus']
        today = datetime.date.today()

        with transaction.atomic():
            Vote.objects.filter(employee=employee, date=today).delete()

            votes = [
                Vote(menu=menu, employee=employee, points=points, date=today)
                for menu, points in zip(menus, [Vote.Points.Top, Vote.Points.Second, Vote.Points.Third])
            ]
            Vote.objects.bulk_create(votes)

        return {"menus": menus, "votes": votes}
