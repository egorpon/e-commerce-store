# E-Commerce Store

Full-stack e-commerce web app built with Django (server-rendered templates, no separate frontend/API layer).

Live: [ecommercepro.site](https://ecommercepro.site)

## Stack

Django · SQLite · Bootstrap 4 (crispy-forms) · DB-backed cart · Gmail SMTP

## Prerequisites

- Python 3.12+
- pip / venv

## Setup

```bash
python -m venv venv
source venv/bin/activate        # windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
SECRET_KEY="your-secret-key"
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
```

## Running

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://localhost:8000`.

## Project layout

```
store/       products, categories, catalog views
cart/        DB-backed cart (Cart/CartItem), CartService, signal merges guest cart into user cart on login
account/     registration, auth, shipping addresses, order history
payment/     checkout, order + order items, confirmation email
coupon/      percent/fixed discount codes
promotion/   time-bound discounts on products/categories
```

## Features

- Product catalog with categories, per-product/category discounts (`promotion`) and coupon codes (`coupon`)
- Cart is DB-backed (`Cart`/`CartItem`); guests are matched by `session_key`, authenticated users by `user` FK
- Checkout flow creates `Order` + `OrderItem`s and emails an order confirmation
- Account management: registration/login, saved shipping address, order history

## Tests

```bash
python manage.py test
```

## CI/CD

GitHub Actions (`.github/workflows/main.yml`): lint (`ruff`) + test on every push to `main`, then deploy over SSH to an EC2 instance running under `supervisor` behind `nginx`.
