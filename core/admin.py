from django.contrib import admin
from .models import Location, Cuisine, Restaurant, Review


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant_count']
    search_fields = ['name']
    
    def restaurant_count(self, obj):
        return obj.restaurants.count()
    restaurant_count.short_description = 'Number of Restaurants'


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant_count']
    search_fields = ['name']
    
    def restaurant_count(self, obj):
        return obj.restaurants.count()
    restaurant_count.short_description = 'Number of Restaurants'


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cuisine', 'location', 'phone', 'average_rating', 'review_count', 'created_at']
    search_fields = ['name', 'address', 'phone']
    list_filter = ['cuisine', 'location', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'average_rating']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'cuisine', 'location')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('average_rating',),
            'classes': ('collapse',)
        }),
    )
    
    def average_rating(self, obj):
        return f"{obj.average_rating()}/5.0"
    average_rating.short_description = 'Average Rating'
    
    def review_count(self, obj):
        return obj.reviews.count()
    review_count.short_description = 'Reviews'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'user', 'rating', 'title', 'created_at']
    search_fields = ['restaurant__name', 'user__username', 'title']
    list_filter = ['rating', 'created_at', 'restaurant']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Review Details', {
            'fields': ('restaurant', 'user', 'rating', 'title', 'text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
