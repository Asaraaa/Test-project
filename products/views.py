from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductSearchForm, ReviewForm
from .models import Product, Cart, CartItem, Review, Order, OrderItem

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all() 
    review_form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'registration/product_detail.html', context)


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
    
    
    return redirect('cart_detail')


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
    return redirect('cart_detail') 

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # If the user submitted the form
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid(): 
            review = form.save(commit=False)  # Create review object 
            review.product = product  
            review.user = request.user  
            review.save()  # Save the review to the database
            return redirect('product_detail', product_id=product.id)  # Redirect to the product detail page
    
    else:
        form = ReviewForm()  # Display an empty form for the initial page load
    
    # Render the review form template with product information
    return render(request, 'registration/product_detail.html', {'form': form, 'product': product})

def product_review_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()  
    review_form = ReviewForm() 
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'registration/product_detail.html', context)

@login_required  
def create_order(request):
    cart = Cart.objects.get(user=request.user)  # Get the user's cart
    
    # Create a new order for the user, with total cost from the cart
    order = Order.objects.create(user=request.user, total_cost=cart.get_total_cost())

    # Loop through each item in the cart and create OrderItem
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order,  
            product=cart_item.product,  
            quantity=cart_item.quantity,  
            price=cart_item.product.price  
        )
    # Clear the cart after the order is created
    cart.cartitem_set.all().delete()

    # Redirect the user to the order summary page
    return redirect('order_summary', order_id=order.id)
from django.shortcuts import get_object_or_404

def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'registration/order_summary.html', {'order': order})
