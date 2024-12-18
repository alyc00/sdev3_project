from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.OrderHistory.as_view(), name='order_history'),
    path('<int:order_id>/', views.OrderDetail.as_view(), name='order_detail'),
]