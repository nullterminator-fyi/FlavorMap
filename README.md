# FlavorMap 🍽️

> CSE 220 — Web Programming • Spring 2026 • Acıbadem University
>
> Restaurant Review & Discovery Platform built with Django.

---

## 📋 Setup Instructions

### Requirements
- Python 3.10+
- uv

### 1. Clone & install dependencies
```bash
git clone <your-repo-url>
cd FlavorMap
uv sync
source .venv/bin/activate
```
> `Pillow` is required by `ImageField` (restaurant photos & avatars).

### 2. Apply migrations
```bash
pythom manage.py makemigrations
python manage.py migrate
```

### 3. (Optional) Create a superuser to use the admin panel
```bash
python manage.py createsuperuser
```

### 4. Populate test data
```bash
python populate_data.py
```
This creates:
- 4 test users (passwords below)
- 7 Istanbul restaurants with coordinates, photos placeholders, menus, opening hours
- 15 reviews + 5 replies + favorites

### 5. Run the server
```bash
python manage.py runserver
```
Open <http://127.0.0.1:8000>.

---

## 🔑 Test Credentials

| Username | Password | Role |
|---|---|---|
| `restaurant_owner` | `testpass123` | Owns all seeded restaurants — can manage menus, edit/delete |
| `testuser1` | `testpass123` | Has reviews + favorites |
| `testuser2` | `testpass123` | Has reviews + favorites |
| `testuser3` | `testpass123` | Has reviews |

The admin panel is at <http://127.0.0.1:8000/admin/> (use the superuser you created).

---

## ✅ Feature Checklist

### Mandatory (all 16 implemented)
- ✅ **Restaurant CRUD** — create/edit/delete with ownership checks
- ✅ **Category System** — Cuisine model + filter dropdown
- ✅ **Location Filter** — Location model + filter dropdown
- ✅ **Price Range Filter** — €/€€/€€€ choices + filter
- ✅ **Reviews & Ratings** — 1–5 stars, title, text, date, one per user
- ✅ **Average Rating** — computed property + sort-by-rating option
- ✅ **Search** — name / description / location / address (`Q` objects, `icontains`)
- ✅ **User Authentication** — register/login/logout + `@login_required` decorators
- ✅ **Menu Management** — `MenuItem` model, owner-only CRUD
- ✅ **Favorites List** — M2M, toggle button, dedicated page
- ✅ **Restaurant Photo** — `ImageField` + `MEDIA_URL`/`MEDIA_ROOT`
- ✅ **Opening Hours** — 7-day schedule per restaurant
- ✅ **Popular Ranking** — Home shows top-rated + newest sections
- ✅ **User Profile** — bio, avatar, reviews, favorites
- ✅ **Review Replies** — one-level nesting via `ReviewReply`
- ✅ **Atomic Transactions** — `transaction.atomic()` + `IntegrityError` handling in register / create_restaurant / review submit

### Bonus
- [x] **Map Integration** — Google Maps iframe on every restaurant detail page (uses coordinates if set, falls back to address search). "Open in Google Maps" button included.
- [x] CSS & Responsive — basic responsive layout included
- [ ] JavaScript Element
- [ ] Restaurant Owner Role
- [ ] Photo Gallery
- [x] Advanced Filtering (partially done — already supports combined cuisine + location + price)
- [x] Review Likes

---

## 🗂️ Project Structure

```
FlavorMap/
├── flavormap/              # Django project (settings, urls)
├── core/                   # Main app
│   ├── models.py           # Restaurant, Cuisine, Location, Review,
│   │                       # ReviewReply, MenuItem, OpeningHours, UserProfile
│   ├── views.py            # All view logic (atomic transactions inside)
│   ├── forms.py            # ModelForms
│   ├── urls.py             # App-level routing
│   └── admin.py            # Admin panel customization
├── templates/
│   ├── base.html
│   ├── core/               # home, restaurant_*, profile, favorites, menu_*
│   └── registration/       # login, register
├── media/                  # Uploaded photos (auto-created)
├── populate_data.py        # Seed script
└── manage.py
```

---

## 🗺️ Data Model (high-level)

```
User ──┬── UserProfile          (1-1)
       ├── created_restaurants  (1-N)
       ├── restaurant_reviews   (1-N)
       ├── review_replies       (1-N)
       └── favorite_restaurants (M-N)

Restaurant ─┬── reviews         (1-N)
            ├── menu_items      (1-N)
            ├── opening_hours   (1-N)
            ├── cuisine         (N-1)
            └── location        (N-1)

Review ── replies (1-N)
```

---

## 🔍 Key URLs

| URL | Description |
|---|---|
| `/` | Home with top-rated + newest restaurants |
| `/restaurants/` | List with search, filters, sort |
| `/restaurants/<id>/` | Detail (photo, hours, menu, reviews, replies, map) |
| `/restaurants/create/` | Create restaurant (auth) |
| `/restaurants/<id>/edit/` | Edit (owner only) |
| `/favorites/` | Logged-in user's favorites |
| `/profile/` | Logged-in user's profile (reviews + favorites) |
| `/admin/` | Django admin |

---

## 🛠 Common issues

- **`Pillow not installed`** — run `pip install Pillow`.
- **Photos not showing** — make sure `DEBUG=True` for development; in production you need a real media server.
- **Map shows wrong place** — set the restaurant's `latitude` / `longitude` (visible in the create/edit form). If empty, the map falls back to searching by address.
- **Re-seeding** — `populate_data.py` deletes test users and seeded restaurants before re-creating. Run it any time.
