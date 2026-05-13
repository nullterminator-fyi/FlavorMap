"""
URL patterns for core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Restaurant CRUD
    path('restaurants/create/', views.create_restaurant, name='create_restaurant'),
    path('restaurants/<int:restaurant_id>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('restaurants/<int:restaurant_id>/delete/', views.delete_restaurant, name='delete_restaurant'),

    # Reviews
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('reviews/<int:review_id>/reply/', views.add_reply, name='add_reply'),
    path('replies/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),

    # Favorites
    path('favorites/', views.favorites_list, name='favorites'),
    path('restaurants/<int:restaurant_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # Menu management
    path('restaurants/<int:restaurant_id>/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
]
