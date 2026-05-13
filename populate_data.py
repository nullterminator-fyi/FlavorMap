"""
Populate FlavorMap with realistic test data.
Run from project root:  python populate_data.py
"""
import os
import django
from datetime import time
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flavormap.settings')
django.setup()

from django.db import transaction
from django.contrib.auth.models import User
from core.models import (
    Location, Cuisine, Restaurant, Review,
    MenuItem, OpeningHours, ReviewReply, UserProfile,
)


# ------------------------------------------------------------------ #
# Reset
# ------------------------------------------------------------------ #
print("Clearing existing data...")
ReviewReply.objects.all().delete()
Review.objects.all().delete()
MenuItem.objects.all().delete()
OpeningHours.objects.all().delete()
Restaurant.objects.all().delete()
Location.objects.all().delete()
Cuisine.objects.all().delete()
UserProfile.objects.all().delete()
User.objects.filter(username__in=[
    'restaurant_owner', 'testuser1', 'testuser2', 'testuser3',
]).delete()


# ------------------------------------------------------------------ #
# Users
# ------------------------------------------------------------------ #
print("Creating users...")
with transaction.atomic():
    owner = User.objects.create_user(
        username='restaurant_owner', email='owner@example.com', password='testpass123'
    )
    UserProfile.objects.create(user=owner, bio='I own a few restaurants in Istanbul.')

    users = []
    for i in range(1, 4):
        u = User.objects.create_user(
            username=f'testuser{i}', email=f'user{i}@example.com', password='testpass123'
        )
        UserProfile.objects.create(user=u, bio=f'Foodie #{i} — always hungry.')
        users.append(u)


# ------------------------------------------------------------------ #
# Locations (Istanbul districts)
# ------------------------------------------------------------------ #
print("Creating locations...")
locations = {
    name: Location.objects.create(name=name, description=desc) for name, desc in [
        ('Kadıköy', 'Vibrant district on the Asian side, cafe-heavy'),
        ('Beşiktaş', 'Busy waterfront area with diverse dining'),
        ('Beyoğlu', 'Heart of the European side, historic and trendy'),
        ('Karaköy', 'Hip neighborhood with specialty coffee and brunch spots'),
        ('Üsküdar', 'Traditional Bosphorus-side district'),
    ]
}


# ------------------------------------------------------------------ #
# Cuisines
# ------------------------------------------------------------------ #
print("Creating cuisines...")
cuisines = {
    name: Cuisine.objects.create(name=name, description=desc) for name, desc in [
        ('Turkish', 'Authentic Turkish dishes — kebab, meze, lahmacun'),
        ('Italian', 'Pasta, pizza, and Mediterranean classics'),
        ('Japanese', 'Sushi, ramen, and modern Japanese cuisine'),
        ('Seafood', 'Fresh fish, mezes, and Bosphorus specialties'),
        ('Fast Food', 'Burgers, fries, and quick bites'),
        ('Italian Fusion', 'Italian classics with a modern twist'),
    ]
}


# ------------------------------------------------------------------ #
# Restaurants — with coordinates for map integration
# ------------------------------------------------------------------ #
print("Creating restaurants...")
restaurants_data = [
    {
        'name': 'Çiya Sofrası',
        'description': 'Legendary spot in Kadıköy serving regional Turkish dishes from across Anatolia. Each visit is a journey through Turkey\'s diverse culinary traditions.',
        'cuisine': cuisines['Turkish'],
        'location': locations['Kadıköy'],
        'address': 'Caferağa Mah., Güneşli Bahçe Sk. No:43, Kadıköy',
        'phone': '(0216) 330-3190',
        'email': 'info@ciya.com.tr',
        'website': 'https://ciya.com.tr',
        'price_range': '€€',
        'latitude': 40.9897,
        'longitude': 29.0286,
    },
    {
        'name': 'Karaköy Lokantası',
        'description': 'Modern take on traditional Turkish meyhane culture with elegant tilework and a curated raki selection.',
        'cuisine': cuisines['Turkish'],
        'location': locations['Karaköy'],
        'address': 'Kemankeş Cad. No:37/A, Karaköy',
        'phone': '(0212) 292-4455',
        'email': 'info@karakoylokantasi.com',
        'website': 'https://karakoylokantasi.com',
        'price_range': '€€€',
        'latitude': 41.0258,
        'longitude': 28.9764,
    },
    {
        'name': 'Sushico Beşiktaş',
        'description': 'Premium sushi and Japanese cuisine with fresh imports and a sleek atmosphere overlooking the Bosphorus.',
        'cuisine': cuisines['Japanese'],
        'location': locations['Beşiktaş'],
        'address': 'Akaretler, Süleyman Seba Cad. No:48, Beşiktaş',
        'phone': '(0212) 327-7700',
        'email': 'info@sushico.com.tr',
        'website': 'https://sushico.com.tr',
        'price_range': '€€€',
        'latitude': 41.0438,
        'longitude': 29.0036,
    },
    {
        'name': 'Mangerie Bebek',
        'description': 'Cozy bistro on the Bosphorus serving Italian-Mediterranean cuisine with a stunning view.',
        'cuisine': cuisines['Italian Fusion'],
        'location': locations['Beşiktaş'],
        'address': 'Cevdetpaşa Cad. No:69, Bebek, Beşiktaş',
        'phone': '(0212) 263-5199',
        'email': 'info@mangeriebebek.com',
        'website': 'https://mangeriebebek.com',
        'price_range': '€€€',
        'latitude': 41.0796,
        'longitude': 29.0428,
    },
    {
        'name': 'Balıkçı Sabahattin',
        'description': 'Iconic seafood restaurant in Sultanahmet area — over 50 years of tradition.',
        'cuisine': cuisines['Seafood'],
        'location': locations['Beyoğlu'],
        'address': 'Cankurtaran Mah., Seyit Hasan Koyu Sok. No:1',
        'phone': '(0212) 458-1824',
        'email': 'info@balikcisabahattin.com',
        'website': 'https://balikcisabahattin.com',
        'price_range': '€€€',
        'latitude': 41.0058,
        'longitude': 28.9784,
    },
    {
        'name': 'Burger Joint Istanbul',
        'description': 'Fast and friendly burger spot with hand-pressed patties and crispy fries.',
        'cuisine': cuisines['Fast Food'],
        'location': locations['Beyoğlu'],
        'address': 'İstiklal Cad. No:120, Beyoğlu',
        'phone': '(0212) 244-1111',
        'email': 'hi@burgerjoint.com.tr',
        'website': 'https://burgerjoint.com.tr',
        'price_range': '€',
        'latitude': 41.0345,
        'longitude': 28.9776,
    },
    {
        'name': 'Locale Italiano',
        'description': 'Wood-fired Neapolitan pizza and homemade pasta in a quaint Üsküdar setting.',
        'cuisine': cuisines['Italian'],
        'location': locations['Üsküdar'],
        'address': 'Salacak Mah., Sahil Yolu No:21, Üsküdar',
        'phone': '(0216) 553-6677',
        'email': 'ciao@localeitaliano.com',
        'website': 'https://localeitaliano.com',
        'price_range': '€€',
        'latitude': 41.0245,
        'longitude': 29.0152,
    },
]

restaurants = []
for data in restaurants_data:
    r = Restaurant.objects.create(created_by=owner, **data)
    restaurants.append(r)


# ------------------------------------------------------------------ #
# Opening Hours — same for all (typical lunch + dinner service)
# ------------------------------------------------------------------ #
print("Creating opening hours...")
default_hours = [
    # (day, open, close, closed)
    (0, time(12, 0), time(23, 0), False),  # Mon
    (1, time(12, 0), time(23, 0), False),  # Tue
    (2, time(12, 0), time(23, 0), False),  # Wed
    (3, time(12, 0), time(23, 0), False),  # Thu
    (4, time(12, 0), time(0, 0),  False),  # Fri
    (5, time(11, 0), time(0, 0),  False),  # Sat
    (6, time(11, 0), time(22, 0), False),  # Sun
]
for r in restaurants:
    # Burger Joint is open later, closed Sundays
    if r.name == 'Burger Joint Istanbul':
        hours = [
            (0, time(11, 0), time(23, 0), False),
            (1, time(11, 0), time(23, 0), False),
            (2, time(11, 0), time(23, 0), False),
            (3, time(11, 0), time(23, 0), False),
            (4, time(11, 0), time(1, 0),  False),
            (5, time(11, 0), time(1, 0),  False),
            (6, None, None, True),  # Sun closed
        ]
    else:
        hours = default_hours
    for day, open_t, close_t, closed in hours:
        OpeningHours.objects.create(
            restaurant=r, day=day,
            open_time=open_t, close_time=close_t, is_closed=closed,
        )


# ------------------------------------------------------------------ #
# Menu Items
# ------------------------------------------------------------------ #
print("Creating menu items...")
menus = {
    'Çiya Sofrası': [
        ('main',    'Etli Ekmek',        'Anatolian-style flatbread with seasoned ground meat.',     Decimal('120.00')),
        ('main',    'İskender Kebap',    'Sliced lamb on pita with tomato sauce and yogurt.',         Decimal('180.00')),
        ('starter', 'Muhammara',         'Walnut and red pepper dip with pomegranate molasses.',      Decimal('55.00')),
        ('dessert', 'Künefe',            'Sweet cheese pastry soaked in syrup.',                       Decimal('90.00')),
        ('drink',   'Ayran',             'Traditional yogurt drink.',                                  Decimal('20.00')),
    ],
    'Karaköy Lokantası': [
        ('main',    'Lamb Tandır',       'Slow-cooked lamb with potatoes and Turkish spices.',         Decimal('260.00')),
        ('starter', 'Meze Platter',      'Selection of 6 traditional mezes.',                          Decimal('180.00')),
        ('dessert', 'Aşure',             'Noah\'s pudding with grains, nuts, and dried fruits.',       Decimal('70.00')),
        ('drink',   'Rakı (single)',     'Anise-flavored Turkish national drink.',                     Decimal('120.00')),
    ],
    'Sushico Beşiktaş': [
        ('main',    'Dragon Roll',       'Eel, avocado, and cucumber with sweet eel sauce.',           Decimal('240.00')),
        ('main',    'Salmon Sashimi',    'Fresh salmon sashimi, 8 pieces.',                            Decimal('280.00')),
        ('starter', 'Edamame',           'Steamed soybeans with sea salt.',                            Decimal('60.00')),
        ('drink',   'Sake (small)',      'Warm Japanese rice wine.',                                   Decimal('110.00')),
    ],
    'Mangerie Bebek': [
        ('main',    'Truffle Pasta',     'Fresh tagliatelle with black truffle and parmesan.',         Decimal('310.00')),
        ('main',    'Sea Bass Carpaccio','Thinly sliced sea bass with citrus and olive oil.',          Decimal('260.00')),
        ('dessert', 'Tiramisu',          'Classic Italian dessert with mascarpone.',                   Decimal('110.00')),
        ('drink',   'House Red Wine',    'Glass of Italian Chianti.',                                  Decimal('130.00')),
    ],
    'Balıkçı Sabahattin': [
        ('main',    'Grilled Sea Bass',  'Whole grilled sea bass with seasonal vegetables.',           Decimal('420.00')),
        ('main',    'Calamari Tava',     'Pan-fried calamari with garlic sauce.',                      Decimal('220.00')),
        ('starter', 'Levrek Marin',      'Marinated sea bass starter.',                                Decimal('150.00')),
        ('drink',   'White Wine Glass',  'Glass of Turkish dry white wine.',                           Decimal('100.00')),
    ],
    'Burger Joint Istanbul': [
        ('main',    'Classic Burger',    '180g beef patty, cheddar, lettuce, tomato.',                 Decimal('150.00')),
        ('main',    'Double Cheese',     'Two patties, double cheddar, special sauce.',                Decimal('210.00')),
        ('side',    'Fries',             'Crispy hand-cut fries with sea salt.',                       Decimal('45.00')),
        ('drink',   'Soda',              'Coke / Sprite / Fanta.',                                     Decimal('30.00')),
    ],
    'Locale Italiano': [
        ('main',    'Margherita Pizza',  'Tomato, mozzarella, basil — Neapolitan style.',              Decimal('165.00')),
        ('main',    'Spaghetti Carbonara','Eggs, guanciale, pecorino, black pepper.',                  Decimal('195.00')),
        ('starter', 'Bruschetta',        'Toasted bread, tomato, basil, garlic.',                      Decimal('70.00')),
        ('dessert', 'Panna Cotta',       'Vanilla cream with berry sauce.',                            Decimal('80.00')),
    ],
}
for r in restaurants:
    for cat, name, desc, price in menus.get(r.name, []):
        MenuItem.objects.create(
            restaurant=r, category=cat, name=name, description=desc, price=price,
        )


# ------------------------------------------------------------------ #
# Reviews + Replies + Favorites
# ------------------------------------------------------------------ #
print("Creating reviews, replies, and favorites...")
reviews_seed = [
    # (restaurant_name, user_index, title, text, rating)
    ('Çiya Sofrası',           0, 'Authentic Anatolian flavors!',  'Every dish tells a story. The künefe was incredible.', 5),
    ('Çiya Sofrası',           1, 'Worth the hype',                'Great variety and the staff was happy to explain each dish.', 5),
    ('Çiya Sofrası',           2, 'Good but crowded',              'Food was excellent, but we waited 40 minutes for a table.', 4),

    ('Karaköy Lokantası',      0, 'Elegant evening',               'Beautiful interior and the lamb tandır was outstanding.', 5),
    ('Karaköy Lokantası',      1, 'Best meze in town',             'Sharing platters were generous and full of flavor.', 5),

    ('Sushico Beşiktaş',       0, 'Premium sushi',                 'Fresh fish and creative rolls. Pricey but worth it.', 5),
    ('Sushico Beşiktaş',       2, 'Solid Japanese option',         'Good ramen, sashimi was very fresh.', 4),

    ('Mangerie Bebek',         1, 'Lovely view, lovely food',      'Truffle pasta was sublime. Reservation recommended.', 5),
    ('Mangerie Bebek',         2, 'Romantic spot',                 'Perfect for special occasions. Pricey but the view!', 4),

    ('Balıkçı Sabahattin',     0, 'Fresh seafood done right',      'The grilled sea bass melted in my mouth.', 5),
    ('Balıkçı Sabahattin',     1, 'Historic and tasty',            'Iconic spot — the calamari was perfect.', 4),

    ('Burger Joint Istanbul',  0, 'Quick and tasty',               'Best burger I\'ve had in Beyoğlu. Fries are amazing.', 4),
    ('Burger Joint Istanbul',  2, 'Solid fast food',               'Quick service, generous portions, fair price.', 4),

    ('Locale Italiano',        1, 'Real Neapolitan pizza',         'Crust was perfect — crispy yet chewy. Great wine list.', 5),
    ('Locale Italiano',        2, 'Hidden gem',                    'Cozy spot with authentic Italian flavors. Loved it!', 4),
]

# Map restaurant name -> instance for fast lookup
by_name = {r.name: r for r in restaurants}

with transaction.atomic():
    for name, ui, title, text, rating in reviews_seed:
        Review.objects.create(
            restaurant=by_name[name],
            user=users[ui],
            title=title,
            text=text,
            rating=rating,
        )

# Add a few replies (owner replying to reviews)
print("Adding replies...")
sample_reviews = Review.objects.all()[:5]
for review in sample_reviews:
    ReviewReply.objects.create(
        review=review,
        user=owner,
        text='Thank you for visiting and for taking the time to write a review! Hope to see you again soon.',
    )

# Add favorites
print("Adding favorites...")
# testuser1 favorites the first 3 restaurants
for r in restaurants[:3]:
    r.favorited_by.add(users[0])
# testuser2 favorites 2
for r in restaurants[3:5]:
    r.favorited_by.add(users[1])


print("\n✅ Database populated successfully!")
print(f"   - {Location.objects.count()} locations")
print(f"   - {Cuisine.objects.count()} cuisines")
print(f"   - {Restaurant.objects.count()} restaurants (all with coordinates for map)")
print(f"   - {OpeningHours.objects.count()} opening hours entries")
print(f"   - {MenuItem.objects.count()} menu items")
print(f"   - {Review.objects.count()} reviews")
print(f"   - {ReviewReply.objects.count()} replies")
print(f"   - {User.objects.filter(username__startswith='testuser').count() + 1} users created")
print("\nLogin credentials:")
print("   restaurant_owner / testpass123  (owns all restaurants — can edit/menu)")
print("   testuser1 / testpass123")
print("   testuser2 / testpass123")
print("   testuser3 / testpass123")
