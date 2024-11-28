from django.shortcuts import render, get_object_or_404
from .models import Genre, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def prod_list(request, genre_id=None):
    genre = None
    products = Product.objects.filter(available=True)

    if genre_id:
        genre = get_object_or_404(Genre, id=genre_id)
        products = Product.objects.filter(genre=genre, available=True)
    
    paginator = Paginator(products, 25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    
    return render(request, '<LINK>.html',{'genre':genre, 'products':products})
    

def product_detail(request, genre_id, product_id):
    product = get_object_or_404(Product, genre_id=genre_id, id=product_id)
    
    return render(request, '<LINK>.html', {'product':product})
 