# HealthPharma - Command Reference Guide

## 🎯 Essential Commands

### Starting the Server
```bash
# Navigate to project directory
cd c:\digicodes\newproject

# Start development server
python manage.py runserver

# Access at http://localhost:8000
```

### Creating Users
```bash
# Create superuser (admin)
python manage.py createsuperuser

# Create regular user via website registration
# Go to http://localhost:8000/register/
```

### Database Operations
```bash
# Create database tables (first time)
python manage.py migrate

# Create migration files for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migrations
python manage.py migrate newapp 0001
```

### Initial Setup
```bash
# Run one-time setup (creates admin, categories, products)
python manage.py setup

# Create fresh database
python manage.py flush  # ⚠️ WARNING: Deletes all data!
```

### Admin Interface
```bash
# Change admin user password
python manage.py changepassword admin

# Create additional superuser
python manage.py createsuperuser
```

### Utility Commands
```bash
# Show SQL for migrations
python manage.py sqlmigrate newapp 0001

# Shell access (Python interactive)
python manage.py shell

# Check for issues
python manage.py check

# Show installed apps
python manage.py showmigrations

# Load data from fixture
python manage.py loaddata fixture_name.json

# Dump data to fixture
python manage.py dumpdata > backup.json
```

## 📁 File Management

### Create Directories (if missing)
```bash
mkdir media
mkdir media\products
mkdir media\categories
mkdir media\prescriptions
mkdir templates
```

### Directory Structure
```
c:\digicodes\newproject\
├── db.sqlite3          ← Database file
├── manage.py           ← Django management
├── media/              ← Uploaded files
├── newapp/             ← App directory
├── newproject/         ← Project config
├── README.md
├── SETUP_GUIDE.md
├── IMPLEMENTATION_SUMMARY.md
└── this_file.md
```

## 🔧 Configuration Commands

### Environment Variables (Optional)
```bash
# Set debug mode
set DJANGO_DEBUG=False

# Set secret key
set DJANGO_SECRET_KEY=your-secret-key

# Set allowed hosts
set DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### Check Deployment Readiness
```bash
python manage.py check --deploy
```

## 🐍 Python/Django Shell Commands

### Access Django Shell
```bash
python manage.py shell
```

### Inside Shell
```python
# Import models
from newapp.models import Product, Category, Order, User

# Create category
Category.objects.create(name='Pain Relief', description='Pain relievers')

# Get all products
products = Product.objects.all()

# Filter products
pain_relief = Product.objects.filter(category__name='Pain Relief')

# Get single product
product = Product.objects.get(id='product-id')

# Update product
product.price = 100
product.save()

# Delete product
product.delete()

# Count products
Product.objects.count()

# Get orders for user
user = User.objects.get(username='username')
orders = user.orders.all()

# Exit shell
exit()
```

## 🗃️ Database Backups

### Backup Database
```bash
# Copy database file
copy db.sqlite3 db.sqlite3.backup

# Or export data
python manage.py dumpdata > backup.json
```

### Restore Database
```bash
# Restore from backup
copy db.sqlite3.backup db.sqlite3

# Or restore from data
python manage.py loaddata backup.json
```

## 📊 Testing & Debugging

### Run Tests (if created)
```bash
python manage.py test
python manage.py test newapp
python manage.py test newapp.tests.YourTest
```

### View Detailed Logs
```bash
# Enable verbose output
python manage.py runserver --verbosity 2
```

### Debug Mode
```bash
# Django debugger
python manage.py runserver --debug
```

## 🚀 Production Deployment Commands

### Prepare for Production
```bash
# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check --deploy

# Create cache table (if using cache)
python manage.py createcachetable

# Create full backup
python manage.py dumpdata > production_backup.json
```

### Use Production Server
```bash
# With Gunicorn (install: pip install gunicorn)
gunicorn newproject.wsgi

# With uWSGI (install: pip install uwsgi)
uwsgi --http :8000 --wsgi-file newproject/wsgi.py --master --processes 4
```

## 📦 Package Management

### Install Required Packages
```bash
pip install django pillow
```

### Upgrade Django
```bash
pip install --upgrade django
```

### Show Installed Packages
```bash
pip list
pip show django
```

### Create Requirements File
```bash
pip freeze > requirements.txt
```

### Install from Requirements
```bash
pip install -r requirements.txt
```

## 🔒 Security Commands

### Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Change Secret Key in settings.py
```python
SECRET_KEY = 'your-new-secret-key'
```

### Set Secure Settings
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🐛 Troubleshooting Commands

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Find process using port
netstat -ano | findstr :8000
taskkill /PID process_id /F
```

### Clear Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

### Reset Migrations
```bash
# ⚠️ WARNING: Only in development!
python manage.py migrate newapp zero
python manage.py migrate newapp
```

### Fix Database Lock
```bash
# Delete corrupted database
del db.sqlite3
python manage.py migrate
python manage.py setup
```

## 📈 Performance Optimization

### Enable Caching
```bash
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### Use Database Connection Pooling
```bash
pip install django-db-connection-pool
```

### Optimize Images
```bash
pip install pillow-simd
```

## 📋 Quick Reference Checklist

- [ ] Database migrated: `python manage.py migrate`
- [ ] Admin user created: `python manage.py setup`
- [ ] Server running: `python manage.py runserver`
- [ ] Can access http://localhost:8000
- [ ] Admin panel works: http://localhost:8000/admin/
- [ ] Registration works
- [ ] Products visible
- [ ] Cart functions
- [ ] Checkout works
- [ ] Admin can manage products

## 🔗 Useful URLs

```
Frontend:
- Home: http://localhost:8000/
- Products: http://localhost:8000/products/
- Cart: http://localhost:8000/cart/
- Register: http://localhost:8000/register/
- Login: http://localhost:8000/login/
- Dashboard: http://localhost:8000/dashboard/
- Admin: http://localhost:8000/admin/

API (if added):
- Product API: http://localhost:8000/api/products/
- Order API: http://localhost:8000/api/orders/
- Cart API: http://localhost:8000/api/cart/
```

## 💾 Data Management

### Export All Data
```bash
python manage.py dumpdata --all --indent 4 > all_data.json
```

### Export Specific Model
```bash
python manage.py dumpdata newapp.Product > products.json
```

### Import Data
```bash
python manage.py loaddata products.json
```

### Clear All Data
```bash
python manage.py flush --noinput
```

## 📞 Common Issues & Solutions

### Issue: ModuleNotFoundError: No module named 'django'
**Solution**: 
```bash
pip install django pillow
```

### Issue: Port 8000 already in use
**Solution**:
```bash
python manage.py runserver 8001
```

### Issue: Static files not loading
**Solution**:
```bash
python manage.py collectstatic --noinput
```

### Issue: Database locked
**Solution**:
```bash
del db.sqlite3
python manage.py migrate
```

### Issue: Migration conflicts
**Solution**:
```bash
python manage.py showmigrations newapp
python manage.py migrate newapp --fake-initial
```

## 🎓 Learning Django Commands

### See Available Commands
```bash
python manage.py help
python manage.py help [command_name]
```

### Example
```bash
python manage.py help runserver
python manage.py help migrate
python manage.py help createsuperuser
```

## 📱 Mobile Testing

### Test on Mobile Device
```bash
# Find your IP
ipconfig

# Run server on all interfaces
python manage.py runserver 0.0.0.0:8000

# Access from mobile: http://your-ip:8000
```

---

## 🚀 Start Your Website Now!

```bash
# Navigate to project
cd c:\digicodes\newproject

# Start server
python manage.py runserver

# Open browser
# Visit http://localhost:8000
```

**Happy Coding!** 💻
