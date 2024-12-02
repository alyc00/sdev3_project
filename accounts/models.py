from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class CustomUser(AbstractUser):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    fav_artist = models.CharField(max_length=255, blank=True)
    fav_album = models.CharField(max_length=255, blank=True)
    fav_genre = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user        
        
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()