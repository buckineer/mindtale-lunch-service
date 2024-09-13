from django.urls import path

from .views import CreateMenuView, CreateRestaurantView

urlpatterns = [
    path('', CreateRestaurantView.as_view(), name='create_restaurant'),
    path('menu/', CreateMenuView.as_view(), name='create_menu'),
]
