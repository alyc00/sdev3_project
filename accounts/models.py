from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        # get_user_model(),
         settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user)
    
class CustomUser(AbstractUser):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"