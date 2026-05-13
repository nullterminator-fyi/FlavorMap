from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Restaurant


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with email"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class RestaurantForm(forms.ModelForm):
    """Form for creating and editing restaurants"""
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'cuisine', 'location', 'address', 'phone', 'email', 'website', 'price_range']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }