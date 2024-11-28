from django.urls import path, include

urlpatterns = [
    #path('', include('pages.urls')), 
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/', include('accounts.urls')),
    #path('', include('pages.urls')),
    path('products/', include('products.urls')),  
    path('search/', include('search.urls')),
]