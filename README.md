# Simple Django Shop

This repository contains a minimal Django project with a `store` app.

Key features:
- `Category` and `Product` models (ForeignKey from Product to Category)
- `is_on_sale` and `discount_price` fields on Product; `has_discount()` helper
- Home page showing all available products sorted by price and category list
- Category pages and a Sale page
- Fixtures to populate the database: `store/fixtures/initial_data.json`

Quickstart:

1. Create and activate a virtualenv (Windows example):

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

2. Run migrations and load fixtures:

```powershell
python manage.py migrate
python manage.py loaddata store/fixtures/initial_data.json
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the site.
