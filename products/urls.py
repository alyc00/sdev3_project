from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.prod_list, name = 'all_products'),
    path('<uuid:genre_id>/', views.prod_list, name = 'products_by_genre'),
    path('<uuid:genre_id>/<uuid:product_id>/', views.product_detail, name = 'product_detail'),
    ]
