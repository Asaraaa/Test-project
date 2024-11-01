from django.urls import path
from .views import register, user_login, home_view, profile_view # Importing the views for registration and login

urlpatterns = [
    path('', home_view, name='home'),  # Home view URL
    path('register/', register, name='register'),  # URL for user registration
    path('login/', user_login, name='login'),  # URL for user login
    path('profile/', profile_view, name='profile') #URL for user profile
]
