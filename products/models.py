from django.db import models
import uuid
from django.urls import reverse


class Genre(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    genre_name = models.CharField(max_length=256, unique=True, blank=False)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(upload_to = 'genre', blank=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


    def get_absolute_url(self):
        return reverse('shop:products_by_genre', args=[self.id])

    def __str__(self):
        return self.genre_name
    

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    album_name = models.CharField(max_length=256, unique=True, blank=False)
    artist_name = models.CharField(max_length=256, unique=True, blank=False)   
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product', blank=True)
    release_year = models.IntegerField(max_digits=16, blank=False)
    price = models.DecimalField(max_digits=16, decimal_places=2, blank=False)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'


    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.genre.id, self.id])

    def __str__(self):
        return self.album_name
    
    def get_artist(self):
        return self.artist_name

    def get_year(self):
        return self.release_year