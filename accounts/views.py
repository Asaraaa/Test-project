from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm 
from django.contrib.auth import update_session_auth_hash


# User registration form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Customizing the User login form to add 'form-control' class to fields
class UserLoginForm(AuthenticationForm):
    def init(self, *args, kwargs):
        super(UserLoginForm, self).__init__(*args, kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Login successful!')
            return redirect('home')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context)

# Home view
def home_view(request):
    return render(request, 'registration/home.html')

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})

@login_required  
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Saving the form 
            messages.success(request, 'Profile updated successfully!')
            update_session_auth_hash(request, form.instance)  # Correctly using request here
            return redirect('profile')  # Redirect to the profile page after successful update
    else:
        form = UserChangeForm(instance=request.user)  # Populating the form with current user's info

    return render(request, 'registration/edit_profile.html', {'form': form})
