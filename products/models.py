from django.db import models
from django.contrib.auth.models import User
  

class Product(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=100)  # Field for product category

    def __str__(self):
        return self.name

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)  # Link CartItem to Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product added to the cart
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when item is added to the cart

    def total_price(self):  # Calculate total price based on quantity
        return self.quantity * self.product.price


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Cart to a user

    def get_total_cost(self):  # Calculate total cost of all items in the cart
        return sum(item.total_price() for item in self.cartitem_set.all())  # Access CartItems related to this Cart


class Review(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each review to a user
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # Link each review to a product
    rating = models.IntegerField()  # Rating (1 to 5)
    comment = models.TextField()  # Comment field
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp when review is created

    def __str__(self):
        return f"Review by {self.user.username}"

# Order model to store user's orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link order to a user
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Total cost of the order

    def __str__(self):
        return f"Order by {self.user.username}"  # Display user who made the order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Link each order item to an order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link each order item to a product
    quantity = models.PositiveIntegerField()  # Quantity of the product in the order
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product in the order

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}" 

from products.models import Product