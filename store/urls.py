from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('categories/', views.all_categories_view, name='all_categories'),
    path('categories/<int:category_id>/', views.category_detail_view, name='category_detail'),
    path('products/', views.all_products_view, name='all_products'),
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
]
