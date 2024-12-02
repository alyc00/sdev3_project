from django.views.generic import ListView
from .models import Product, Category
from django.shortcuts import render, get_object_or_404

class StoreView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Add ordering if needed
        return Product.objects.select_related('category').all()

# view all products
def all_products_view(request):
    products = Product.objects.filter(available=True)
    return render(request, 'store/all_products.html', {'products': products})

# View for product detail
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})
    
def all_categories_view(request):
    categories = Category.objects.all()
    return render(request, 'store/categories.html', {'categories': categories})

# View for a specific category
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })