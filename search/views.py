from products.models import Product
from django.views.generic import ListView
from django.db.models import Q


class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'search.html'


    def get_queryset(self):
        query = self.request.GET.get('q')

        return Product.objects.filter(
                Q(album_name__icontains=query) | 
                Q(artist_name__icontains=query) |
                Q(genre__icontains=query) |
                Q(release_year__icontains=query) |
                Q(description__icontains=query))
                # can search by name of album or artist, or by genre or year


    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')

        return context

