from django.urls import path

from .views import TopVotedMenuView

urlpatterns = [
    path('top_voted_menu/', TopVotedMenuView.as_view(), name='top-voted-menu'),
]
