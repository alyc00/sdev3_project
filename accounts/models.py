from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )