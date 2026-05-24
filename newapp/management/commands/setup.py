from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from newapp.models import CompanyInfo, Category, Product
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Setup initial data for Healeaf Pharma'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@healeafpharma.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('[OK] Created superuser: admin (password: admin123)'))
        else:
            self.stdout.write('Superuser already exists')

        # Create company info
        if not CompanyInfo.objects.exists():
            CompanyInfo.objects.create(
                company_name='Healeaf Pharma',
                phone='+91-1800-123-4567',
                email='support@healeafpharma.com',
                address='123 Medical Plaza, Healthcare Street',
                city='Mumbai',
                state='Maharashtra',
                zip_code='400001',
                about='Healeaf Pharma is your trusted online pharmacy providing authentic medicines and healthcare products at affordable prices. We are committed to making healthcare accessible to everyone.'
            )
            self.stdout.write(self.style.SUCCESS('[OK] Created company information'))
        else:
            self.stdout.write('Company info already exists')

        # Create categories
        categories_data = [
            ('Pain Relief', 'Painkillers, Anti-inflammatory medicines'),
            ('Cold & Cough', 'Cold syrups, cough tablets, nasal sprays'),
            ('Antibiotics', 'Antibiotic tablets and injections'),
            ('Vitamins & Supplements', 'Multivitamins, calcium, iron supplements'),
            ('Skin Care', 'Creams, ointments, skincare products'),
            ('Digestive Health', 'Antacids, digestive tablets, probiotics'),
            ('Blood Pressure', 'BP control medicines'),
            ('Diabetes', 'Diabetes management products'),
        ]

        for cat_name, cat_desc in categories_data:
            if not Category.objects.filter(name=cat_name).exists():
                Category.objects.create(name=cat_name, description=cat_desc)
                self.stdout.write(self.style.SUCCESS(f'[OK] Created category: {cat_name}'))

        # Create sample products
        products_data = [
            {
                'name': 'Aspirin 500mg',
                'generic_name': 'Acetylsalicylic Acid',
                'category_name': 'Pain Relief',
                'description': 'Effective pain reliever and fever reducer. Used for headaches, muscle pain, and minor arthritis pain.',
                'price': Decimal('25.00'),
                'discount_price': Decimal('20.00'),
                'stock': 100,
                'unit': 'tablet',
                'strength': '500mg',
                'manufacturer': 'Generic Pharma',
                'requires_prescription': False,
            },
            {
                'name': 'Paracetamol Syrup',
                'generic_name': 'Paracetamol',
                'category_name': 'Cold & Cough',
                'description': 'Safe and effective fever and pain relief syrup for children and adults.',
                'price': Decimal('85.00'),
                'discount_price': Decimal('70.00'),
                'stock': 50,
                'unit': 'syrup',
                'strength': '125mg/5ml',
                'manufacturer': 'Health Labs',
                'requires_prescription': False,
            },
            {
                'name': 'Amoxicillin 500mg',
                'generic_name': 'Amoxicillin',
                'category_name': 'Antibiotics',
                'description': 'Antibiotic medication used to treat bacterial infections.',
                'price': Decimal('150.00'),
                'discount_price': None,
                'stock': 30,
                'unit': 'capsule',
                'strength': '500mg',
                'manufacturer': 'Antibiotic Co',
                'requires_prescription': True,
            },
            {
                'name': 'Multivitamin Tablet',
                'generic_name': 'Multivitamin',
                'category_name': 'Vitamins & Supplements',
                'description': 'Complete daily multivitamin to boost immunity and energy levels.',
                'price': Decimal('200.00'),
                'discount_price': Decimal('150.00'),
                'stock': 80,
                'unit': 'tablet',
                'strength': 'Daily Formula',
                'manufacturer': 'Vitality Plus',
                'requires_prescription': False,
            },
            {
                'name': 'Cough Syrup',
                'generic_name': 'Dextromethorphan',
                'category_name': 'Cold & Cough',
                'description': 'Effective cough suppressant for dry and wet coughs.',
                'price': Decimal('120.00'),
                'discount_price': Decimal('90.00'),
                'stock': 60,
                'unit': 'syrup',
                'strength': '10mg/5ml',
                'manufacturer': 'Cough Relief Inc',
                'requires_prescription': False,
            },
        ]

        expiry_date = date.today() + timedelta(days=365)

        for product_data in products_data:
            category_name = product_data.pop('category_name')
            category = Category.objects.get(name=category_name)
            
            if not Product.objects.filter(name=product_data['name']).exists():
                product_data['category'] = category
                product_data['expiry_date'] = expiry_date
                Product.objects.create(**product_data)
                self.stdout.write(self.style.SUCCESS(f"[OK] Created product: {product_data['name']}"))

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Setup completed successfully!'))
        self.stdout.write(self.style.WARNING('\nLogin with:'))
        self.stdout.write(self.style.WARNING('  Username: admin'))
        self.stdout.write(self.style.WARNING('  Password: admin123'))
