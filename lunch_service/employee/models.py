from django.db import models

from lunch_service.authentication.models import User
from lunch_service.restaurant.models import Menu

# Create your models here.


class Vote(models.Model):
    class Points(models.IntegerChoices):
        Top = 3
        Second = 2
        Third = 1

    employee: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    menu: models.ForeignKey = models.ForeignKey(Menu, on_delete=models.CASCADE)
    points: models.IntegerField = models.IntegerField(choices=Points.choices, default=Points.Top)
    date: models.DateField = models.DateField(auto_now_add=True)
