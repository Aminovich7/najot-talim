# LuxWatch — Django Watch Shop

## Setup
```bash
pip install django pillow
python manage.py migrate
python manage.py runserver
```

## Demo Accounts
| Username     | Password   | Role  |
|-------------|------------|-------|
| admin        | admin123   | Admin |
| horologist   | pass1234   | Seller|
| collector    | pass1234   | Seller|

## Features
- Auth: Signup, Login, Logout, Edit Profile, Change Password
- Products: List, Detail, Create, Edit, Delete (owner only)
- My Watches: personal dashboard table
- Search & filter by category, condition, price range
- Luxury dark/gold UI theme
