from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductSearchForm
from .models import Product, Cart, CartItem

def product_detail(request, product_id):
    return HttpResponse(f"This is the detail page for product ID {product_id}.")

def product_list(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()  # Fetching all products from the database

    if form.is_valid():
        query = form.cleaned_data.get('query')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        category = form.cleaned_data.get('category')

        if query:
            products = products.filter(name__icontains=query)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)

        if category:
            products = products.filter(category=category)

    context = {
        'form': form,
        'products': products
    }
    return render(request, 'registration/product_list.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID, or show a 404 error
    cart, created = Cart.objects.get_or_create(user=request.user)  # Get the user's cart or create it if it doesn't exist
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  # Get or create the cart item for the product

    if not created: 
        cart_item.quantity += 1  # Increase the quantity of the cart item by 1
        cart_item.save()  

    return redirect('registration/cart_detail.html') 

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()  # Get all items in the cart
    return render(request, 'registration/cart_detail.html', {'cart': cart, 'cart_items': cart_items})

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity = int(request.POST.get('quantity'))
    item.save() 
    return redirect('registration/cart_detail.html')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('registration/cart_detail.html')