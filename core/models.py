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
    PRICE_RANGES = [
        ('€', 'Budget (€)'),
        ('€€', 'Moderate (€€)'),
        ('€€€', 'Expensive (€€€)'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    price_range = models.CharField(max_length=3, choices=PRICE_RANGES, default='€')

    # NEW — restaurant photo (mandatory)
    photo = models.ImageField(upload_to='restaurants/', blank=True, null=True)

    # NEW — coordinates for map integration (bonus)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # NEW — favorites M2M (mandatory)
    favorited_by = models.ManyToManyField(User, related_name='favorite_restaurants', blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_restaurants', null=True)
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

    def review_count(self):
        return self.reviews.count()


class OpeningHours(models.Model):
    """Opening hours per day of the week for a restaurant (mandatory)"""
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.IntegerField(choices=DAY_CHOICES)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['day']
        unique_together = ('restaurant', 'day')
        verbose_name_plural = 'Opening Hours'

    def __str__(self):
        if self.is_closed:
            return f"{self.restaurant.name} - {self.get_day_display()}: Closed"
        return f"{self.restaurant.name} - {self.get_day_display()}: {self.open_time}-{self.close_time}"


class MenuItem(models.Model):
    """Menu items for a restaurant (mandatory)"""
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
        ('side', 'Side'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


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

    def score(self):
        """Calculate net score based on likes and dislikes"""
        likes = self.like_dislikes.filter(score=LikeDislike.Score.LIKE).count() * LikeDislike.Score.LIKE
        dislikes = self.like_dislikes.filter(score=LikeDislike.Score.DISLIKE).count() * LikeDislike.Score.DISLIKE
        return likes + dislikes

class ReviewReply(models.Model):
    """One-level reply to a review (mandatory)"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Review Replies'

    def __str__(self):
        return f"Reply by {self.user.username} on review #{self.review.id}"


class UserProfile(models.Model):
    """Extended user profile (mandatory — user profile page)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
class LikeDislike(models.Model):
    """Model to track user likes and dislikes on reviews"""
    class Score(models.IntegerChoices):
        LIKE = 1, 'Like'
        NONE = 0, 'None'
        DISLIKE = -1, 'Dislike'

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='like_dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_likes_dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    score = models.IntegerField(choices=Score)
    
    class Meta:
        unique_together = ('review', 'user')
