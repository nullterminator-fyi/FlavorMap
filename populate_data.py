import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flavormap.settings')
django.setup()

from core.models import Location, Cuisine, Restaurant, Review
from django.contrib.auth.models import User

# Clear existing data
Location.objects.all().delete()
Cuisine.objects.all().delete()
Restaurant.objects.all().delete()
Review.objects.all().delete()
User.objects.filter(username__startswith='testuser').delete()

print("Creating test user for restaurants...")
test_user = User.objects.create_user(username='restaurant_owner', email='owner@example.com', password='testpass123')

print("Creating locations...")
locations = [
    Location.objects.create(name='Downtown', description='Heart of the city with modern restaurants'),
    Location.objects.create(name='Midtown', description='Central area with diverse dining options'),
    Location.objects.create(name='East Side', description='Residential area with family-friendly restaurants'),
    Location.objects.create(name='West End', description='Trendy neighborhood with hip eateries'),
    Location.objects.create(name='Arts District', description='Cultural hub with upscale dining'),
]

print("Creating cuisines...")
cuisines = [
    Cuisine.objects.create(name='Italian', description='Traditional and modern Italian cuisine'),
    Cuisine.objects.create(name='Indian', description='Authentic Indian spices and flavors'),
    Cuisine.objects.create(name='Japanese', description='Sushi, ramen, and Japanese specialties'),
    Cuisine.objects.create(name='Mexican', description='Traditional Mexican dishes and fusion'),
    Cuisine.objects.create(name='French', description='Classic French bistro and fine dining'),
    Cuisine.objects.create(name='Thai', description='Authentic Thai cuisine with bold flavors'),
    Cuisine.objects.create(name='Chinese', description='Traditional and contemporary Chinese cooking'),
]

print("Creating restaurants...")
restaurants = [
    Restaurant.objects.create(
        name='The Gourmet Kitchen',
        description='Authentic Italian cuisine with fresh ingredients and traditional recipes passed down through generations. Our chef sources the finest ingredients from local suppliers.',
        cuisine=cuisines[0],
        location=locations[0],
        address='123 Main St, Downtown',
        phone='(555) 123-4567',
        email='info@gourmetkitchen.com',
        website='https://gourmetkitchen.com',
        created_by=test_user
    ),
    Restaurant.objects.create(
        name='Spice Route',
        description='Aromatic Indian dishes prepared with the finest spices and traditional methods. Experience the rich flavors of Indian cuisine in an elegant setting.',
        cuisine=cuisines[1],
        location=locations[1],
        address='456 Oak Ave, Midtown',
        phone='(555) 234-5678',
        email='info@spiceroute.com',
        website='https://spiceroute.com',
        created_by=test_user
    ),
    Restaurant.objects.create(
        name='Sakura Sushi',
        description='Premium sushi and Japanese cuisine crafted by experienced chefs trained in Tokyo. Fresh fish delivered daily for the finest sushi experience.',
        cuisine=cuisines[2],
        location=locations[2],
        address='789 Elm St, East Side',
        phone='(555) 345-6789',
        email='info@sakurasushi.com',
        website='https://sakurasushi.com',
        created_by=test_user
    ),
    Restaurant.objects.create(
        name='El Mariachi',
        description='Vibrant Mexican flavors bringing the spirit of Mexico to your table. Family recipes and modern twists on traditional dishes.',
        cuisine=cuisines[3],
        location=locations[3],
        address='321 Pine Rd, West End',
        phone='(555) 456-7890',
        email='info@elmariachi.com',
        website='https://elmariachi.com',
        created_by=test_user
    ),
    Restaurant.objects.create(
        name='Le Petit Bistro',
        description='Classic French bistro with an extensive wine selection and exquisite cuisine. Intimate ambiance perfect for romantic dinners.',
        cuisine=cuisines[4],
        location=locations[4],
        address='654 Maple Dr, Arts District',
        phone='(555) 567-8901',
        email='info@lepetitbistro.com',
        website='https://lepetitbistro.com',
        created_by=test_user
    ),
    Restaurant.objects.create(
        name='Bangkok Street',
        description='Authentic Thai street food with bold flavors and fresh ingredients. Popular for pad thai, curry, and tom yum soup.',
        cuisine=cuisines[5],
        location=locations[0],
        address='234 Willow Ave, Downtown',
        phone='(555) 678-9012',
        email='info@bangkokstreet.com',
        website='https://bangkokstreet.com',
        created_by=test_user
    ),
    Restaurant.objects.create(
        name='Dynasty Garden',
        description='Contemporary Chinese cuisine with traditional cooking techniques. Dim sum served daily with excellent selection.',
        cuisine=cuisines[6],
        location=locations[1],
        address='567 Birch Ln, Midtown',
        phone='(555) 789-0123',
        email='info@dynastygarden.com',
        website='https://dynastygarden.com',
        created_by=test_user
    ),
]

print("Creating test users...")
users = [
    User.objects.create_user(username='testuser1', email='user1@example.com', password='testpass123'),
    User.objects.create_user(username='testuser2', email='user2@example.com', password='testpass123'),
    User.objects.create_user(username='testuser3', email='user3@example.com', password='testpass123'),
]

print("Creating reviews...")
reviews_data = [
    # The Gourmet Kitchen reviews
    {
        'restaurant': restaurants[0],
        'user': users[0],
        'title': 'Amazing Italian Food!',
        'text': 'Had the best carbonara I\'ve ever tasted. The pasta was perfectly cooked and the sauce was authentic. Highly recommend!',
        'rating': 5
    },
    {
        'restaurant': restaurants[0],
        'user': users[1],
        'title': 'Great atmosphere and taste',
        'text': 'The restaurant has a lovely ambiance with soft lighting. The tiramisu for dessert was phenomenal.',
        'rating': 4
    },
    {
        'restaurant': restaurants[0],
        'user': users[2],
        'title': 'Good but pricey',
        'text': 'Food quality is excellent but portions could be larger for the price. Still worth visiting.',
        'rating': 4
    },
    # Spice Route reviews
    {
        'restaurant': restaurants[1],
        'user': users[0],
        'title': 'Authentic Indian flavors',
        'text': 'This restaurant really captures the essence of Indian cuisine. The biryani was outstanding and the naan was perfectly baked.',
        'rating': 5
    },
    {
        'restaurant': restaurants[1],
        'user': users[1],
        'title': 'Excellent curry!',
        'text': 'The butter chicken was creamy and delicious. Great selection of wines too. Will definitely come back.',
        'rating': 5
    },
    {
        'restaurant': restaurants[1],
        'user': users[2],
        'title': 'Good but spicy',
        'text': 'If you like spicy food, this is the place. Make sure to ask for mild if you\'re sensitive to heat.',
        'rating': 4
    },
    # Sakura Sushi reviews
    {
        'restaurant': restaurants[2],
        'user': users[0],
        'title': 'Best sushi in town!',
        'text': 'Fresh, quality fish and skilled preparation. The sashimi platter was a work of art. Worth every penny.',
        'rating': 5
    },
    {
        'restaurant': restaurants[2],
        'user': users[1],
        'title': 'Great sushi experience',
        'text': 'The chef was very attentive and the rolls were creative. Love the Japanese beer selection.',
        'rating': 4
    },
    # El Mariachi reviews
    {
        'restaurant': restaurants[3],
        'user': users[0],
        'title': 'Authentic Mexican cuisine',
        'text': 'The mole sauce was incredible and the margaritas are some of the best I\'ve had. Great place to celebrate!',
        'rating': 5
    },
    {
        'restaurant': restaurants[3],
        'user': users[2],
        'title': 'Fun and tasty',
        'text': 'Great atmosphere, friendly staff, and delicious food. The guacamole is made fresh at your table.',
        'rating': 4
    },
    # Le Petit Bistro reviews
    {
        'restaurant': restaurants[4],
        'user': users[1],
        'title': 'Perfect romantic dinner spot',
        'text': 'Intimate setting, excellent French wine selection, and impeccable service. The coq au vin was superb.',
        'rating': 5
    },
    {
        'restaurant': restaurants[4],
        'user': users[2],
        'title': 'Classic French elegance',
        'text': 'Beautiful decor and sophisticated menu. Prix fixe was a good value for the quality.',
        'rating': 5
    },
    # Bangkok Street reviews
    {
        'restaurant': restaurants[5],
        'user': users[0],
        'title': 'Authentic pad thai!',
        'text': 'tastes just like street food in Bangkok. Cooking is fast and flavors are vibrant.',
        'rating': 5
    },
    {
        'restaurant': restaurants[5],
        'user': users[1],
        'title': 'Good and affordable',
        'text': 'Great value for money. The curry is spicy but delicious. Fast service too.',
        'rating': 4
    },
    # Dynasty Garden reviews
    {
        'restaurant': restaurants[6],
        'user': users[0],
        'title': 'Excellent dim sum!',
        'text': 'The shrimp dumplings were delicate and flavorful. Great selection and reasonable prices.',
        'rating': 4
    },
    {
        'restaurant': restaurants[6],
        'user': users[2],
        'title': 'Modern take on classics',
        'text': 'They do traditional dishes well but also add creative twists. Loved the dessert selection.',
        'rating': 4
    },
]

for review_data in reviews_data:
    Review.objects.create(**review_data)

print("\n✅ Database populated successfully!")
print(f"   - {len(locations)} locations created")
print(f"   - {len(cuisines)} cuisines created")
print(f"   - {len(restaurants)} restaurants created")
print(f"   - {len(users)} test users created")
print(f"   - {len(reviews_data)} reviews created")
