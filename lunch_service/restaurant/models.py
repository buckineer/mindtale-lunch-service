import secrets

from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    """
    Later, we should create APIKeyModel if we have to support APIKey Authentication to other business or djangorestframework-api-key packages.
    But now, for simplicity, stored api_key on Restaurant model directly.
    """
    name: models.CharField = models.CharField(max_length=255)
    api_key: models.CharField = models.CharField(max_length=255, unique=True, default=secrets.token_urlsafe)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_urlsafe(settings.LUNCH_SERVICE_API_KEY_LENGTH)
        super().save(*args, **kwargs)


class Menu(models.Model):
    """
    Later, For extendabitliy and scalability, Item model should be introduced, and connected with ForeignKey with Menu Model.
    But now, for simplicity, used items attribute as TextField.
    """
    restaurant: models.ForeignKey = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date: models.DateField = models.DateField()
    items: models.TextField = models.TextField()

    # voted_points=models.IntegerField()    # can have this field in the future to optimize the response time of selecting menu for lunch. Instead of using aggregation query in Vote Model.
