# LuxWatch — Django watch shop

A small marketplace for luxury watches built with Django templates. Registered users can list their own watches for sale and manage them from a personal dashboard.

## Features

- Custom user model with sign-up, login, logout, profile editing and password change
- Product list and detail pages with search and filters by category, condition and price range
- "My watches" dashboard: create, edit and delete your own listings (owner-only permissions)
- Django admin for categories, products and users
- Dark / gold UI theme

## Stack

Python, Django (function-based views, ModelForms, custom user model), SQLite, Pillow for product images and avatars.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd watchshop_project/watchshop
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configuration

`SECRET_KEY` and `DEBUG` are read from environment variables (see `.env.example`). If they are not set, the project falls back to development defaults, so it runs locally out of the box.

| Variable | Default |
|---|---|
| `DJANGO_SECRET_KEY` | a development-only key |
| `DJANGO_DEBUG` | `True` |
