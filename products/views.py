from django.http import HttpResponse
from django.shortcuts import render  
from .models import Product 

def product_detail(request, product_id):
    return HttpResponse(f"This is the detail page for product ID {product_id}.")


def product_list(request): 
    products = Product.objects.all()  # Fetching all products from the database
    return render(request, 'registration/product_list.html', {'products': products}) 

