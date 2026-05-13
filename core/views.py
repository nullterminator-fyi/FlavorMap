from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.db import transaction, IntegrityError
from django.http import HttpResponseForbidden

from .models import (
    Restaurant, Cuisine, Location, Review,
    MenuItem, ReviewReply, UserProfile, OpeningHours,
)
from .forms import (
    CustomUserCreationForm, RestaurantForm, ReviewForm,
    ReviewReplyForm, MenuItemForm, UserProfileForm,
)


# ------------------------------------------------------------------ #
# AUTH
# ------------------------------------------------------------------ #
def register(request):
    """User registration view — atomic to ensure profile is created with user"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    # Create empty profile alongside user
                    UserProfile.objects.create(user=user)
                    login(request, user)
                    messages.success(request, 'Welcome to FlavorMap!')
                    return redirect('core:home')
            except IntegrityError:
                messages.error(request, 'Could not create your account. Please try again.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {
        'page_title': 'Register',
        'form': form,
    })


# ------------------------------------------------------------------ #
# HOME — top-rated + newest sections
# ------------------------------------------------------------------ #
def home(request):
    all_restaurants = Restaurant.objects.annotate(avg=Avg('reviews__rating'))

    # Top rated (only those with at least 1 review)
    top_rated = (
        all_restaurants
        .filter(reviews__isnull=False)
        .order_by('-avg', '-created_at')
        .distinct()[:3]
    )
    # Newest
    newest = Restaurant.objects.order_by('-created_at')[:3]

    return render(request, 'core/home.html', {
        'page_title': 'Home',
        'message': 'Welcome to FlavorMap - Discover Amazing Restaurants',
        'top_rated': top_rated,
        'newest': newest,
    })


# ------------------------------------------------------------------ #
# RESTAURANT LIST — search + filters + sort
# ------------------------------------------------------------------ #
def restaurant_list(request):
    restaurants = Restaurant.objects.select_related('cuisine', 'location').annotate(
        avg=Avg('reviews__rating')
    )

    # Search
    q = request.GET.get('q', '').strip()
    if q:
        restaurants = restaurants.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(location__name__icontains=q) |
            Q(address__icontains=q)
        )

    # Filters
    cuisine_filter = request.GET.get('cuisine')
    location_filter = request.GET.get('location')
    price_filter = request.GET.get('price_range')

    if cuisine_filter:
        restaurants = restaurants.filter(cuisine__id=cuisine_filter)
    if location_filter:
        restaurants = restaurants.filter(location__id=location_filter)
    if price_filter:
        restaurants = restaurants.filter(price_range=price_filter)

    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'rating':
        restaurants = restaurants.order_by('-avg', '-created_at')
    elif sort == 'name':
        restaurants = restaurants.order_by('name')
    else:  # newest
        restaurants = restaurants.order_by('-created_at')

    return render(request, 'core/restaurant_list.html', {
        'page_title': 'Restaurants',
        'restaurants': restaurants,
        'cuisines': Cuisine.objects.all(),
        'locations': Location.objects.all(),
        'q': q,
        'sort': sort,
    })


# ------------------------------------------------------------------ #
# RESTAURANT DETAIL — reviews + replies + menu + hours + favorites + map
# ------------------------------------------------------------------ #
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(
        Restaurant.objects.prefetch_related('reviews__replies', 'menu_items', 'opening_hours'),
        id=restaurant_id,
    )
    reviews = restaurant.reviews.all()

    review_form = None
    user_review = None
    is_favorited = False

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        is_favorited = restaurant.favorited_by.filter(id=request.user.id).exists()

        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=user_review) if user_review else ReviewForm(request.POST)
            if form.is_valid():
                try:
                    # Atomic: review save + restaurant updated_at refresh together
                    with transaction.atomic():
                        review = form.save(commit=False)
                        review.restaurant = restaurant
                        review.user = request.user
                        review.save()
                        # touch restaurant so updated_at refreshes
                        restaurant.save(update_fields=['updated_at'])
                    messages.success(request, 'Review submitted successfully!')
                    return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
                except IntegrityError:
                    messages.error(request, 'Could not save review (you may already have one).')
        else:
            review_form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    # Build hours dict so the template can iterate 0..6 in order
    hours_by_day = {h.day: h for h in restaurant.opening_hours.all()}

    return render(request, 'core/restaurant_detail.html', {
        'page_title': restaurant.name,
        'restaurant': restaurant,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'is_favorited': is_favorited,
        'reply_form': ReviewReplyForm(),
        'hours_by_day': hours_by_day,
        'day_labels': OpeningHours.DAY_CHOICES,
    })


# ------------------------------------------------------------------ #
# REVIEW REPLIES
# ------------------------------------------------------------------ #
@login_required
def add_reply(request, review_id):
    """Reply to a review (one level of nesting)"""
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            reply.save()
            messages.success(request, 'Reply added.')
    return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)


@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(ReviewReply, id=reply_id)
    if reply.user != request.user:
        return HttpResponseForbidden('Not your reply.')
    restaurant_id = reply.review.restaurant.id
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted.')
    return redirect('core:restaurant_detail', restaurant_id=restaurant_id)


# ------------------------------------------------------------------ #
# STATIC PAGES
# ------------------------------------------------------------------ #
def about(request):
    return render(request, 'core/about.html', {
        'page_title': 'About',
        'about_text': 'FlavorMap is your guide to discovering exceptional restaurants in your area. '
                      'We provide honest reviews, ratings, and recommendations from food enthusiasts like you.',
    })


def contact(request):
    return render(request, 'core/contact.html', {
        'page_title': 'Contact',
        'contact_email': 'info@flavormap.com',
        'contact_phone': '(555) 999-9999',
        'message': 'Get in touch with us for any questions or suggestions.',
    })


# ------------------------------------------------------------------ #
# RESTAURANT CRUD
# ------------------------------------------------------------------ #
@login_required
def create_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Atomic: restaurant + default opening hours together
                with transaction.atomic():
                    restaurant = form.save(commit=False)
                    restaurant.created_by = request.user
                    restaurant.save()
                    # default 7 opening-hour rows so the table is never empty
                    for day, _ in OpeningHours.DAY_CHOICES:
                        OpeningHours.objects.create(
                            restaurant=restaurant, day=day, is_closed=True
                        )
                messages.success(request, 'Restaurant created successfully!')
                return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
            except IntegrityError:
                messages.error(request, 'Could not save restaurant. Please try again.')
    else:
        form = RestaurantForm()

    return render(request, 'core/restaurant_form.html', {
        'page_title': 'Create Restaurant',
        'form': form,
    })


@login_required
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if restaurant.created_by != request.user:
        messages.error(request, 'You can only edit restaurants you created.')
        return redirect('core:restaurant_detail', restaurant_id=restaurant.id)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'core/restaurant_form.html', {
        'page_title': f'Edit {restaurant.name}',
        'form': form,
        'restaurant': restaurant,
    })


@login_required
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if restaurant.created_by != request.user:
        messages.error(request, 'You can only delete restaurants you created.')
        return redirect('core:restaurant_detail', restaurant_id=restaurant.id)

    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, 'Restaurant deleted successfully!')
        return redirect('core:restaurant_list')

    return render(request, 'core/restaurant_confirm_delete.html', {
        'page_title': f'Delete {restaurant.name}',
        'restaurant': restaurant,
    })


# ------------------------------------------------------------------ #
# REVIEW DELETE
# ------------------------------------------------------------------ #
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('core:restaurant_detail', restaurant_id=review.restaurant.id)

    return render(request, 'core/review_confirm_delete.html', {
        'page_title': f'Delete Review for {review.restaurant.name}',
        'review': review,
    })


# ------------------------------------------------------------------ #
# FAVORITES
# ------------------------------------------------------------------ #
@login_required
def toggle_favorite(request, restaurant_id):
    """Add or remove a restaurant from the current user's favorites."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if restaurant.favorited_by.filter(id=request.user.id).exists():
        restaurant.favorited_by.remove(request.user)
        messages.info(request, f'Removed "{restaurant.name}" from favorites.')
    else:
        restaurant.favorited_by.add(request.user)
        messages.success(request, f'Added "{restaurant.name}" to favorites.')
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('core:restaurant_detail', restaurant_id=restaurant.id)


@login_required
def favorites_list(request):
    favorites = request.user.favorite_restaurants.select_related('cuisine', 'location').all()
    return render(request, 'core/favorites.html', {
        'page_title': 'My Favorites',
        'favorites': favorites,
    })


# ------------------------------------------------------------------ #
# MENU MANAGEMENT
# ------------------------------------------------------------------ #
@login_required
def add_menu_item(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if restaurant.created_by != request.user:
        messages.error(request, 'Only the owner can manage the menu.')
        return redirect('core:restaurant_detail', restaurant_id=restaurant.id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            messages.success(request, 'Menu item added.')
            return redirect('core:restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = MenuItemForm()

    return render(request, 'core/menu_item_form.html', {
        'page_title': f'Add Menu Item — {restaurant.name}',
        'form': form,
        'restaurant': restaurant,
    })


@login_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if item.restaurant.created_by != request.user:
        messages.error(request, 'Only the owner can edit menu items.')
        return redirect('core:restaurant_detail', restaurant_id=item.restaurant.id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated.')
            return redirect('core:restaurant_detail', restaurant_id=item.restaurant.id)
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'core/menu_item_form.html', {
        'page_title': f'Edit Menu Item — {item.name}',
        'form': form,
        'restaurant': item.restaurant,
    })


@login_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if item.restaurant.created_by != request.user:
        return HttpResponseForbidden('Not your menu.')
    restaurant_id = item.restaurant.id
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted.')
    return redirect('core:restaurant_detail', restaurant_id=restaurant_id)


# ------------------------------------------------------------------ #
# USER PROFILE
# ------------------------------------------------------------------ #
@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    user_reviews = request.user.restaurant_reviews.select_related('restaurant').all()
    favorites = request.user.favorite_restaurants.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=profile_obj)

    return render(request, 'core/profile.html', {
        'page_title': 'My Profile',
        'profile_obj': profile_obj,
        'form': form,
        'user_reviews': user_reviews,
        'favorites': favorites,
    })
