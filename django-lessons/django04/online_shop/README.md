# 🛒 NajotShop — Django Online Do'kon

Najot Ta'lim | Python & Django yo'nalishi amaliy loyihasi.

## 📁 Loyiha Tuzilmasi

```
online_shop/
├── config/                  ← Django sozlamalari
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                    ← Asosiy ilova
│   ├── migrations/
│   ├── templates/shop/      ← HTML shablonlar
│   │   ├── base.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── product_form.html
│   │   ├── product_confirm_delete.html
│   │   ├── category_list.html
│   │   ├── category_form.html
│   │   └── category_confirm_delete.html
│   ├── fixtures/
│   │   └── sample_data.json ← Namuna ma'lumotlar
│   ├── models.py            ← Product, Category modellari
│   ├── views.py             ← CRUD views
│   ├── urls.py              ← URL yo'nalishlari
│   ├── forms.py             ← Django forms
│   └── admin.py
├── media/                   ← Yuklangan rasmlar
├── manage.py
└── requirements.txt
```

## 🚀 Ishga Tushirish

### 1. Virtual muhit yaratish
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Migratsiyalar
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Superuser yaratish (admin panel uchun)
```bash
python manage.py createsuperuser
```

### 5. Namuna ma'lumotlar yuklash (ixtiyoriy)
```bash
python manage.py loaddata shop/fixtures/sample_data.json
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

Brauzerda oching: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

---

## 🔗 URL Yo'nalishlari

| URL | View | Tavsif |
|-----|------|--------|
| `/` | product_list | Mahsulotlar ro'yxati |
| `/product/<id>/` | product_detail | Mahsulot tafsiloti |
| `/product/create/` | product_create | Yangi mahsulot qo'shish |
| `/product/<id>/update/` | product_update | Mahsulotni tahrirlash |
| `/product/<id>/delete/` | product_delete | Mahsulotni o'chirish |
| `/categories/` | category_list | Kategoriyalar ro'yxati |
| `/categories/create/` | category_create | Yangi kategoriya |
| `/categories/<id>/update/` | category_update | Kategoriyani tahrirlash |
| `/categories/<id>/delete/` | category_delete | Kategoriyani o'chirish |

---

## ✅ CRUD Amallari

- **C**reate — Mahsulot / kategoriya qo'shish
- **R**ead   — Ro'yxat ko'rish, tafsilot sahifasi
- **U**pdate — Tahrirlash formasi
- **D**elete — O'chirishni tasdiqlash sahifasi

## 🛠️ Texnologiyalar

- **Backend**: Django 4.2, SQLite
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Fonts**: Google Fonts (Syne + DM Sans)
- **Media**: Pillow (rasm yuklash)
