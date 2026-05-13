from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Restaurant, Review, ReviewReply, MenuItem, UserProfile, OpeningHours


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with email"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class RestaurantForm(forms.ModelForm):
    """Form for creating and editing restaurants (now with photo + coords)"""
    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'cuisine', 'location',
            'address', 'phone', 'email', 'website', 'price_range',
            'photo', 'latitude', 'longitude',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'e.g. 41.0082'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'e.g. 28.9784'}),
        }


class ReviewForm(forms.ModelForm):
    """Form for creating and editing reviews"""
    class Meta:
        model = Review
        fields = ['title', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class ReviewReplyForm(forms.ModelForm):
    """Form for replying to a review (one level of nesting)"""
    class Meta:
        model = ReviewReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a reply...'}),
        }


class MenuItemForm(forms.ModelForm):
    """Form for adding/editing menu items"""
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class OpeningHoursForm(forms.ModelForm):
    """Form for editing opening hours"""
    class Meta:
        model = OpeningHours
        fields = ['day', 'open_time', 'close_time', 'is_closed']
        widgets = {
            'open_time': forms.TimeInput(attrs={'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'type': 'time'}),
        }
