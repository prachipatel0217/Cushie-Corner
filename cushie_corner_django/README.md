# Cushie Corner - Django E-commerce Website

A beautiful, fully functional Django e-commerce website for Cushie Corner cushion shop.

## Features
- Animated hero section with parallax effect
- Responsive design (mobile, tablet, desktop)
- Product catalog with hover effects and reveal animations
- Session-based shopping cart (add, remove, update quantity)
- Full checkout flow with order placement
- SQLite database with Django ORM
- Contact form with database storage
- Django Admin panel for managing products, orders, and messages

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Setup Script (creates DB + sample data + admin user)
```bash
python setup.py
```

### 3. Start the Server
```bash
python manage.py runserver
```

### 4. Open in Browser
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
  - Username: `admin`
  - Password: `admin123`

## Project Structure
```
cushie_corner_django/
├── cushie_corner/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── store/                  # Main app
│   ├── models.py           # Product, CartItem, Order, ContactMessage
│   ├── views.py            # All view logic
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   ├── templates/store/    # HTML templates
│   │   ├── index.html      # Homepage
│   │   ├── cart.html       # Cart page
│   │   ├── checkout.html   # Checkout form
│   │   └── order_success.html
│   └── static/store/
│       ├── css/style.css   # All styles
│       ├── js/main.js      # Animations, cart JS
│       ├── js/cart.js      # Cart page interactions
│       └── images/         # Product & brand images
├── manage.py
├── setup.py                # One-click setup
└── requirements.txt
```

## Database Models
- **Product** - name, description, price, image, stock
- **CartItem** - session-based cart items
- **Order** - customer details, total, status tracking
- **OrderItem** - line items per order
- **ContactMessage** - form submissions

## Admin Panel
Manage everything from the Django Admin:
- Add/edit products with images and prices
- View and update order statuses
- Read customer contact messages
- Monitor cart activity
