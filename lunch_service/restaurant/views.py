from rest_framework import generics

from lunch_service.authentication.permissions import IsCompanyAdmin, IsRestaurant

from .serializers import MenuSerializer, RestaurantSerializer


class CreateRestaurantView(generics.CreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsCompanyAdmin]


class CreateMenuView(generics.CreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsRestaurant]

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.restaurant)
