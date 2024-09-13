from rest_framework import serializers

from .models import Menu, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('api_key', )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ('restaurant',)


class RestaurantReadWithOutAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ('api_key',)


class MenuWithRestaurantSerializer(MenuSerializer):
    restaurant = RestaurantReadWithOutAPIKeySerializer()
