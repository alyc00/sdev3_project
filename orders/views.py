from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, ListView
from .models import Order, OrderItem



class OrderHistory(LoginRequiredMixin, ListView):
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Retrieve only the orders for the logged-in user
        return Order.objects.filter(user=self.request.user).order_by('-created')


class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order = Order.objects.get(id=order_id, emailAddress=email)
            order_items = OrderItem.objects.filter(order=order)
        
        return render(
            request,
            'order/order_detail.html',
            {
                'order': order,
                'order_items': order_items
            }
        )
