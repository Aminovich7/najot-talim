# Django lessons

Homework and exam projects from my Django course (March–April 2026), collected in one repository. Each folder was originally a separate repository and keeps its original name. They cover models and the ORM, function-based and class-based views, ModelForms, templates, the admin and authentication with a custom user model.

| Folder | What it covers | Run from |
|---|---|---|
| [django02](django02) | Pharmacy (dorixona) inventory and sales, querying PostgreSQL directly with psycopg2 | `django02/` |
| [django03](django03) | Three starter projects: school (students, teachers), shop (products, orders), blog (posts, comments) | `django03/01/`<br>`django03/02/`<br>`django03/03/` |
| [django04](django04) | Online shop: category and product CRUD with ModelForms and templates | `django04/online_shop/` |
| [dars04](dars04) | Book catalogue: authors, categories and a many-to-many book–category link | `dars04/` |
| [django05](django05) | Phone catalogue CRUD with function-based views and templates | `django05/` |
| [Imtihon](Imtihon) | Exam project: services and categories CRUD with templates (the nested `imtihon/` folder is an earlier draft) | `Imtihon/`<br>`Imtihon/imtihon/` |
| [django06](django06) | Phone store CRUD with class-based generic views (ListView, CreateView, UpdateView, DeleteView) | `django06/` |
| [django_auth001](django_auth001) | Custom user model with sign-up, login and logout | `django_auth001/signup_project/` |

## Running a project

Every folder in the **Run from** column is a standalone Django project with its own `manage.py` and SQLite database.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd dars04
python manage.py migrate
python manage.py runserver
```

## Configuration

Settings read their secrets from environment variables (listed in `.env.example`). If they are not set, the projects fall back to development defaults, so they run locally out of the box.

| Variable | Default |
|---|---|
| `DJANGO_SECRET_KEY` | a development-only key |
| `DJANGO_DEBUG` | `True` |
| `PG_HOST`, `PG_PORT`, `PG_DATABASE`, `PG_USER`, `PG_PASSWORD` | used only by `django02`, which queries PostgreSQL with psycopg2 (`django02/dorixona_x.sql` creates its tables) |
