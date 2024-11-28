from django.contrib import admin
from .models import Genre, Product


class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name']

admin.site.register(Genre, GenreAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['album_name', 'artist_name', 'genre', 'release_year', 'price', 'available', 'created', 'updated']
    list_editable = ['price', 'available']

admin.site.register(Product, ProductAdmin)
