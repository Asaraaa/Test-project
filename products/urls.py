from django.urls import path
from .views import product_list, product_detail, product_review_detail # Importing views for products
from . import views

urlpatterns = [
    path('', product_list, name='product_list'),  # URL for listing products
    path('cart/', views.cart_detail, name='cart_detail'),  # URL for viewing cart details
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # URL for adding a product to the cart
    path('cart/update/<int:item_id>/', views.update_quantity, name='update_quantity'),  # URL for updating the quantity of an item
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # URL for removing an item from the cart
    path('<int:product_id>/add_review/', views.add_review, name='add_review'),  # URL for review
    path('<int:product_id>/', views.product_detail, name='product_detail'), # URL for product details
    path('reviews/<int:product_id>/', views.product_review_detail, name='review_detail'),
    path('create_order/', views.create_order, name='create_order'),  # URL for creating an order
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),  # URL for order summary
]
