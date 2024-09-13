# employee_management/urls.py

from django.urls import path

from .views import CreateEmployeeView, VoteView

urlpatterns = [
    path('', CreateEmployeeView.as_view(), name='create_employee'),
    path('vote/', VoteView.as_view(), name='vote_menu'),
]
