"""
URL patterns for core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
