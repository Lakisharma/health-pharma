# HealthPharma - Complete Online Pharmacy Website

A fully functional online pharmacy website built with Django. This is a complete e-commerce solution for health and pharmaceutical products with user authentication, shopping cart, orders, prescriptions, and admin management.

## Features

### User Features
✅ **User Registration & Authentication** - Create accounts, login, logout, manage profile
✅ **Product Browsing** - View products with filtering, search, and categories
✅ **Shopping Cart** - Add/remove products, update quantities, view cart summary
✅ **Orders** - Place orders, track order status, view order history
✅ **Prescription Management** - Upload and verify prescriptions for prescription-required medicines
✅ **Product Reviews & Ratings** - Leave reviews and ratings for products
✅ **User Dashboard** - Central hub for orders, prescriptions, and account management
✅ **Contact Form** - Send messages to the business
✅ **Responsive Design** - Works on desktop, tablet, and mobile devices

### Admin Features
✅ **Comprehensive Admin Panel** - Manage all aspects of the business
✅ **Product Management** - Add, edit, delete products with images
✅ **Category Management** - Organize products into categories
✅ **Order Management** - Track and update order status
✅ **Prescription Verification** - Verify user prescriptions
✅ **User Management** - Manage user accounts
✅ **Contact Messages** - View and respond to customer inquiries
✅ **Review Management** - Manage product reviews

## Technology Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite (default, can be changed)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS for AJAX functionality
- **Icons**: Font Awesome 6.4.0
- **Python Version**: 3.8+

## Project Structure

```
newproject/
├── newapp/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── products.html
│   │   ├── product_detail.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── dashboard.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   ├── order_detail.html
│   │   ├── prescriptions.html
│   │   ├── upload_prescription.html
│   │   ├── contact.html
│   │   └── about.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── newproject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── media/
├── templates/
├── manage.py
└── db.sqlite3
```

## Installation & Setup

### 1. Clone the Repository
```bash
cd c:\digicodes\newproject
```

### 2. Create Virtual Environment (if not already created)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django pillow
```

### 4. Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 6. Create Company Info (Required)
After running migrations, go to admin panel and add company information:
- Login to admin panel at `/admin/`
- Add a CompanyInfo entry with your pharmacy details

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Models

### CompanyInfo
- Store pharmacy business information and details

### Category
- Product categories (Medicines, Supplements, Medical Devices, etc.)

### Product
- Medicine/healthcare products with:
  - Name, Generic Name, Strength
  - Price and Discount Price
  - Stock management
  - Prescription requirement flag
  - Expiry date tracking
  - Manufacturer information
  - Ratings

### Review
- User reviews and ratings for products

### Prescription
- User-uploaded prescriptions with verification status
- Doctor information and file storage

### Cart & CartItem
- Shopping cart functionality
- Items management

### Order & OrderItem
- Order creation and tracking
- Order items and pricing
- Shipping address
- Payment method and status
- Prescription requirement handling

### ContactMessage
- Contact form submissions

## Key Views & URLs

### Public Pages
- `/` - Home page
- `/products/` - Products listing page
- `/products/<id>/` - Product detail page
- `/about/` - About Us page
- `/contact/` - Contact Us page

### Authentication
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout

### User Dashboard
- `/dashboard/` - User dashboard
- `/profile/` - Edit profile
- `/prescriptions/` - My prescriptions
- `/upload-prescription/` - Upload prescription

### Shopping
- `/cart/` - View shopping cart
- `/add-to-cart/` - Add product to cart (AJAX)
- `/update-cart-item/<id>/` - Update cart item (AJAX)
- `/remove-from-cart/<id>/` - Remove from cart
- `/checkout/` - Checkout page
- `/order-confirmation/<id>/` - Order confirmation
- `/order/<id>/` - Order details

## Admin Panel

Access admin panel at `/admin/` with your superuser credentials.

### Admin Features:
1. **Product Management**
   - Create, read, update, delete products
   - Manage inventory and pricing
   - Set discount prices
   - Upload product images

2. **Order Management**
   - View all orders
   - Update order status
   - Manage payment information
   - View order items

3. **Prescription Management**
   - Verify uploaded prescriptions
   - Add notes for users
   - Track prescription status

4. **User Management**
   - View all registered users
   - Manage user accounts

5. **Reporting & Analytics**
   - Contact messages view

## Payment Integration

Currently supports 3 payment methods:
- **Cash on Delivery (COD)** - Default
- **Online Payment** - Framework ready
- **UPI Payment** - Framework ready

To integrate with actual payment gateways (Razorpay, PayPal, etc.), update the checkout process in `views.py`.

## Security Features

- ✅ CSRF Protection
- ✅ Password validation
- ✅ Login required for sensitive operations
- ✅ User-specific data access (orders, cart, etc.)
- ✅ Admin-only access control

## Customization

### Add New Product Categories
1. Go to Admin Panel
2. Navigate to Categories
3. Click "Add Category"
4. Enter category name and description

### Manage Inventory
1. Go to Admin Panel
2. Navigate to Products
3. Edit product stock quantity

### Update Company Information
1. Go to Admin Panel
2. Navigate to Company Info
3. Update details like phone, email, address, logo

## Troubleshooting

### Images not loading
- Ensure media folder exists: `mkdir media`
- Check MEDIA_ROOT and MEDIA_URL settings

### Database errors
- Delete `db.sqlite3`
- Run migrations again: `python manage.py migrate`

### Template not found
- Check template folder paths in settings.py
- Ensure all HTML files are in correct directories

## Future Enhancements

- [ ] Payment gateway integration (Razorpay/PayPal)
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Wishlist feature
- [ ] Product recommendations
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Inventory auto-reorder system

## Production Deployment

Before deploying to production:
1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set secure secret key
5. Enable HTTPS
6. Collect static files: `python manage.py collectstatic`
7. Use gunicorn or similar WSGI server

## License

This project is open source and available under the MIT License.

## Support

For support and questions, please contact through the contact form on the website or reach out to the pharmacy directly.

---

**Happy Coding! 🚀**

Built with ❤️ for Online Pharmacies
