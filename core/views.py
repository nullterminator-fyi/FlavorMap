from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Cuisine, Location, Review


def home(request):
    """Home page view"""
    featured_restaurants = Restaurant.objects.all()[:3]
    
    context = {
        'page_title': 'Home',
        'message': 'Welcome to FlavorMap - Discover Amazing Restaurants',
        'featured_restaurants': featured_restaurants,
    }
    return render(request, 'core/home.html', context)


def restaurant_list(request):
    """Restaurant listing page"""
    restaurants = Restaurant.objects.select_related('cuisine', 'location').all()
    cuisine_filter = request.GET.get('cuisine')
    location_filter = request.GET.get('location')
    
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine__id=cuisine_filter)
    
    if location_filter:
        restaurants = restaurants.filter(location__id=location_filter)
    
    cuisines = Cuisine.objects.all()
    locations = Location.objects.all()
    
    context = {
        'page_title': 'Restaurants',
        'restaurants': restaurants,
        'cuisines': cuisines,
        'locations': locations,
    }
    return render(request, 'core/restaurant_list.html', context)


def restaurant_detail(request, restaurant_id):
    """Individual restaurant detail page"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = restaurant.reviews.all()
    
    context = {
        'page_title': restaurant.name,
        'restaurant': restaurant,
        'reviews': reviews,
    }
    return render(request, 'core/restaurant_detail.html', context)


def about(request):
    """About page"""
    context = {
        'page_title': 'About',
        'about_text': 'FlavorMap is your guide to discovering exceptional restaurants in your area. We provide honest reviews, ratings, and recommendations from food enthusiasts like you.',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page"""
    context = {
        'page_title': 'Contact',
        'contact_email': 'info@flavormap.com',
        'contact_phone': '(555) 999-9999',
        'message': 'Get in touch with us for any questions or suggestions.',
    }
    return render(request, 'core/contact.html', context)
