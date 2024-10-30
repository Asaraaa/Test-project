from django.contrib import admin
from django.urls import path, include 
from accounts.views import home_view  # Importing home_view from accounts views

urlpatterns = [
    path('', home_view, name='home'),  # Home view URL
    path('admin/', admin.site.urls),  # admin panel
    path('accounts/', include('accounts.urls')),  # Including URLs from the accounts app
    path('products/', include('products.urls')),  # Including URLs from the products app
]