from django.db import models
from django.conf import settings
from recipes.models import Recipe

USER_MODEL = settings.AUTH_USER_MODEL


class MealPlan(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateField()
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe, related_name="recipes")
