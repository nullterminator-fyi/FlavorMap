from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from .models import Restaurant, Cuisine, Location, Review, LikeDislike
from .forms import CustomUserCreationForm, RestaurantForm, ReviewForm


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'page_title': 'Register',
        'form': form,
    }
    return render(request, 'registration/register.html', context)


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
    price_filter = request.GET.get('price_range')
    
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine__id=cuisine_filter)
    
    if location_filter:
        restaurants = restaurants.filter(location__id=location_filter)
    
    if price_filter:
        restaurants = restaurants.filter(price_range=price_filter)
    
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
    reviews = restaurant.reviews.select_related('user').prefetch_related('like_dislikes')
    reviews = reviews.annotate(vote_score=Coalesce(Sum('like_dislikes__score'), Value(0))).order_by('-vote_score', '-created_at')
    
    review_form = None
    user_review = None
    user_vote_map = {}
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if request.method == 'POST':
            if user_review:
                form = ReviewForm(request.POST, instance=user_review)
            else:
                form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.user = request.user
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
        else:
            if user_review:
                review_form = ReviewForm(instance=user_review)
            else:
                review_form = ReviewForm()

        votes = LikeDislike.objects.filter(user=request.user, review__restaurant=restaurant)
        user_vote_map = {vote.review_id: vote.score for vote in votes}
    
    for review in reviews:
        review.user_vote_score = user_vote_map.get(review.id, 0)
    
    context = {
        'page_title': restaurant.name,
        'restaurant': restaurant,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'core/restaurant_detail.html', context)


@login_required
def vote_review(request, review_id):
    """Handle like/dislike toggles for a review"""
    review = get_object_or_404(Review, id=review_id)
    if request.method != 'POST':
        return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)

    try:
        score = int(request.POST.get('vote', '0'))
    except ValueError:
        score = 0

    if score not in (LikeDislike.Score.LIKE, LikeDislike.Score.DISLIKE):
        return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)

    like_dislike, created = LikeDislike.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'score': score},
    )

    if not created:
        if like_dislike.score == score:
            like_dislike.score = LikeDislike.Score.NONE
        else:
            like_dislike.score = score
        like_dislike.save()

    return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)


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


@login_required
def create_restaurant(request):
    """Create a new restaurant"""
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.created_by = request.user
            restaurant.save()
            messages.success(request, 'Restaurant created successfully!')
            return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm()
    
    context = {
        'page_title': 'Create Restaurant',
        'form': form,
    }
    return render(request, 'core/restaurant_form.html', context)


@login_required
def edit_restaurant(request, restaurant_id):
    """Edit an existing restaurant (only by creator)"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if restaurant.created_by != request.user:
        messages.error(request, 'You can only edit restaurants you created.')
        return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
    
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)
    
    context = {
        'page_title': f'Edit {restaurant.name}',
        'form': form,
        'restaurant': restaurant,
    }
    return render(request, 'core/restaurant_form.html', context)


@login_required
def delete_review(request, review_id):
    """Delete a review (only by author)"""
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)
    
    context = {
        'page_title': f'Delete Review for {review.restaurant.name}',
        'review': review,
    }
    return render(request, 'core/review_confirm_delete.html', context)


@login_required
def delete_restaurant(request, restaurant_id):
    """Delete a restaurant (only by creator)"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if restaurant.created_by != request.user:
        messages.error(request, 'You can only delete restaurants you created.')
        return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
    
    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, 'Restaurant deleted successfully!')
        return redirect('core:restaurant_list')
    
    context = {
        'page_title': f'Delete {restaurant.name}',
        'restaurant': restaurant,
    }
    return render(request, 'core/restaurant_confirm_delete.html', context)
