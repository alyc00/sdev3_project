from django.urls import path
from . import views

# -------------------------------
app_name = 'cart'
# -------------------------------

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),    
    # Add to cart view
    path('add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),  
    # Cart details view
    path('', views.cart_detail, name='cart_detail'),
    # Remove item from cart
    path('remove/<uuid:product_id>/', views.cart_remove, name='remove_from_cart'),  
    # Clear item from cart
    path('clear_cart/<uuid:product_id>/', views.clear_cart, name='clear_cart'),  
]
