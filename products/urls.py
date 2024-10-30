from django.urls import path
from .views import product_list, product_detail  # Importing views for products

urlpatterns = [
    path('', product_list, name='product_list'),  # URL for listing products
    path('<int:id>/', product_detail, name='product_detail'),  # URL for product detail by ID
]