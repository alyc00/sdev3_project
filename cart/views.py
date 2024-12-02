from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product  
from .models import Cart, CartItem
from django.conf import settings
from orders.models import Order, OrderItem
import stripe
# Voucher
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):  
    product = get_object_or_404(Product, id=product_id)  
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)  
        cart_item.qty += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, qty=1)  
        cart_item.save()
    return redirect('cart:cart_detail')

def clear_cart(request):
    """Clear all items from the user's cart."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        CartItem.objects.filter(cart=cart).delete()  # Delete all items in the cart
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_detail')  # Redirect to cart detail or another page

def cart_detail(request, total=0, counter=0, cart_items=None):
    # voucher
    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            if cart_item.qty > 1:
                cart_item.qty = 1
            counter += cart_item.qty
            total += (cart_item.product.price * cart_item.qty)  
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Product Store - New Order'  # Updated description
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    # Voucher
    voucher_apply_form = VoucherApplyForm()

    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if voucher is not None:
            discount = (total * (voucher.discount / Decimal('100')))
            new_total = (total - discount)
            stripe_total = int(new_total * 100)
    except ObjectDoesNotExist:
        pass

    # End Voucher

    if request.method == 'POST':
        print(request.POST)
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']

            customer = stripe.Customer.create(email=email, source=token)
            stripe.Charge.create(amount=stripe_total, currency="eur",
                                 description=description, customer=customer.id)

            # Creating the order
            try:
                order_details = Order.objects.create(
                    token=token,
                    total=new_total if voucher else total,  
                    emailAddress=email,
                )
                order_details.save()

                if voucher is not None:
                    order_details.voucher = voucher
                    order_details.discount = discount
                order_details.save()

                for order_item in cart_items:
                    ord_it = OrderItem.objects.create(
                        product=order_item.product.name,  
                        price=order_item.product.price,  
                        order=order_details
                    )
                    clear_cart(request, order_item.product.id)
                    if voucher is not None:
                        discount = (ord_it.price * (voucher.discount / Decimal('100')))
                        ord_it.price = (ord_it.price - discount)

                    ord_it.save()

                print('The order has been created')


            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as stripeError:
            return stripeError

    # return context variables
    return render(request,
                  'cart.html',
                  {
                      'cart_items': cart_items,
                      'total': total,
                      'counter': counter,
                      'data_key': data_key,
                      'stripe_total': stripe_total,
                      'description': description,
                      'voucher_apply_form': voucher_apply_form,
                      'new_total': new_total,
                      'voucher': voucher,
                      'discount': discount,
                  }
                  )


def cart_remove(request, product_id):  
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)  
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.qty > 1:
        cart_item.qty -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    # voucher
    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None

    cart_items = []  # Initialize cart_items to an empty list to avoid errors

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the user's cart
        cart_items = CartItem.objects.filter(cart=cart, active=True)  # Get all active items in the cart
        
        for cart_item in cart_items:
            counter += cart_item.qty  # Increment counter by quantity of items
            total += (cart_item.product.price * cart_item.qty)  # Add item subtotal to total

    except ObjectDoesNotExist:
        pass  # If cart doesn't exist, cart_items stays as an empty list

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Product Store - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    
    # Voucher handling
    voucher_apply_form = VoucherApplyForm()

    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if voucher is not None:
            discount = (total * (voucher.discount / Decimal('100')))
            new_total = (total - discount)
            stripe_total = int(new_total * 100)
    except ObjectDoesNotExist:
        pass

    # Handle POST request for Stripe payments
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']

            customer = stripe.Customer.create(email=email, source=token)
            stripe.Charge.create(amount=stripe_total, currency="eur",
                                description=description, customer=customer.id)

            # Create the order
            order_details = Order.objects.create(
                token=token,
                total=new_total if voucher else total,
                emailAddress=email,
            )
            if voucher:
                order_details.voucher = voucher
                order_details.discount = discount
            order_details.save()

            for order_item in cart_items:
                OrderItem.objects.create(
                    product=order_item.product.name,
                    price=order_item.product.price,
                    order=order_details
                )       

        # Clear the cart and redirect to the home page
            clear_cart(request)  # Clear all items from the cart
            return redirect('home')  # Redirect to home page after order completion

        except stripe.error.CardError as stripeError:
            return stripeError


    return render(request,
                  'cart.html',
                  {
                      'cart_items': cart_items,
                      'total': total,
                      'counter': counter,
                      'data_key': data_key,
                      'stripe_total': stripe_total,
                      'description': description,
                      'voucher_apply_form': voucher_apply_form,
                      'new_total': new_total,
                      'voucher': voucher,
                      'discount': discount,
                  }
                  )




def checkout(request):
    if request.method == 'POST':
        # Process payment logic (e.g., Stripe or PayPal)

        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total=calculate_cart_total(request),  # Replace with your cart total calculation
        )

        # Add items to the order
        cart = get_cart_items(request)  # Replace with your cart retrieval logic
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],  # Replace with your product field
                quantity=item['quantity'],
                price=item['price'],
            )

        # Clear the cart after checkout
        clear_cart(request)

        # Redirect to a success page
        return redirect('orders:order_history')