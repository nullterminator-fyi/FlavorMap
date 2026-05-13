from django.contrib import admin
from .models import (
    Location, Cuisine, Restaurant, Review,
    MenuItem, OpeningHours, ReviewReply, UserProfile,
)


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


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cuisine', 'location', 'price_range', 'phone',
                    'avg_rating_display', 'review_count', 'created_at']
    search_fields = ['name', 'address', 'phone', 'description']
    list_filter = ['cuisine', 'location', 'price_range', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'avg_rating_display']
    inlines = [OpeningHoursInline, MenuItemInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'cuisine', 'location', 'price_range', 'photo')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Map Coordinates', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',),
        }),
        ('Ownership', {
            'fields': ('created_by', 'favorited_by'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'avg_rating_display'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('favorited_by',)

    def avg_rating_display(self, obj):
        return f"{obj.average_rating()}/5.0"
    avg_rating_display.short_description = 'Average Rating'

    def review_count(self, obj):
        return obj.reviews.count()
    review_count.short_description = 'Reviews'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'user', 'rating', 'title', 'created_at']
    search_fields = ['restaurant__name', 'user__username', 'title']
    list_filter = ['rating', 'created_at', 'restaurant']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'created_at']
    search_fields = ['user__username', 'text']
    list_filter = ['created_at']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price']
    search_fields = ['name', 'restaurant__name']
    list_filter = ['category', 'restaurant']


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'get_day_display', 'open_time', 'close_time', 'is_closed']
    list_filter = ['day', 'is_closed', 'restaurant']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username', 'bio']
