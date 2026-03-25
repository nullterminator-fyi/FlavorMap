from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):
    """Geographic location for restaurants"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Cuisine(models.Model):
    """Cuisine type/category for restaurants"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cuisines'
    
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    """Restaurant entity with details and relationships"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def average_rating(self):
        """Calculate average rating from all reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0


class Review(models.Model):
    """User reviews for restaurants"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_reviews')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('restaurant', 'user')
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}/5 by {self.user.username}"
