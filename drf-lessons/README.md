# Django REST Framework lessons

Homework and exam projects from my Django REST Framework course (April–June 2026), collected in one repository. Each folder was originally a separate repository and keeps its original name. They go from function-based `@api_view` endpoints through `APIView`, generic views and ViewSets with routers, to custom user models, token and JWT authentication, permissions and OpenAPI documentation.

| Folder | What it covers | Run from |
|---|---|---|
| [restframework01_a](restframework01_a) | First API: watch endpoints with function-based `@api_view` views and a serializer | `restframework01_a/rest01_a/` |
| [restframework01_b](restframework01_b) | Watch CRUD API with function-based `@api_view` views | `restframework01_b/rest01_b/` |
| [djangorestframework](djangorestframework) | Watch CRUD with class-based `APIView` | `djangorestframework/rest02/` |
| [rest03](rest03) | Tool CRUD with generic views: `ListAPIView`, `CreateAPIView`, `RetrieveAPIView`, `UpdateAPIView`, `DestroyAPIView` | `rest03/` |
| [rest04](rest04) | Watch CRUD with `GenericAPIView` and a `ViewSet` registered on a `DefaultRouter` | `rest04/` |
| [rest05](rest05) | Serializer-driven create, update and search endpoints for watches | `rest05/` |
| [rest06](rest06) | Custom user model and sign-up with DRF token authentication | `rest06/` |
| [rest07](rest07) | Users (author profiles with avatars) and posts; OpenAPI docs with drf-spectacular | `rest07/` |
| [rest08](rest08) | Sign-up, login, profile view/update/delete with token auth and `IsAuthenticated`; Swagger docs with drf-yasg | `rest08/` |
| [rest09](rest09) | Blog posts and comments; token auth, custom permissions, change password, logout | `rest09/` |
| [rest10a](rest10a) | JWT authentication with SimpleJWT: sign-up, login, logout with token blacklist, profile, change password | `rest10a/` |
| [rest11](rest11) | Exam project: e-commerce API with accounts, categories, products, cart, orders, payments, reviews, wishlist and notifications; JWT auth, email verification codes, drf-spectacular docs | `rest11/` |

## Running a project

Every folder in the **Run from** column is a standalone Django project with its own `manage.py` and SQLite database.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd rest09
python manage.py migrate
python manage.py runserver
```

## Configuration

Settings read their secrets from environment variables (listed in `.env.example`). If they are not set, the projects fall back to development defaults, so they run locally out of the box.

| Variable | Default |
|---|---|
| `DJANGO_SECRET_KEY` | a development-only key |
| `DJANGO_DEBUG` | `True` |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | empty; used only by `rest11` to email verification codes |
