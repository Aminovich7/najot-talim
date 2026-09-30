# Klinika boshqaruvi (mini)

A small clinic management system built with Django templates: signed-in staff manage doctors, consultations, surgeries and rooms, with report pages.

## Features

- Custom user model with registration, login, profile update and logout
- CRUD for doctors, consultations, surgeries and rooms (login required)
- Report pages for consultations, surgeries and rooms, plus a combined total report
- Django admin for all models

## Stack

Python, Django (class-based generic views with LoginRequiredMixin, ModelForms, custom user model), SQLite, Pillow for avatars.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd project_x
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
