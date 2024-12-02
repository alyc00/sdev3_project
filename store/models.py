from django.db import models
import uuid
from django.urls import reverse

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/categories', blank=True) 
    
    class Meta:
        ordering = ('name',) 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'  # Plural name for the Category model
    
    def get_absolute_url(self):
        return reverse('store:all_product', args=[self.id])

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/products', blank=True, null=True)
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)   

    def __str__(self):
        return self.name
