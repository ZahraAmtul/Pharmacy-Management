from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pharmacy.models import Supplier, Medicine, Customer
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample data for pharmacy management system'

    def handle(self, *args, **options):
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@pharmacy.com', 'admin123')
            self.stdout.write('Created superuser: admin/admin123')

        # Create suppliers
        supplier1, _ = Supplier.objects.get_or_create(
            name="MedSupply Co.",
            defaults={
                'contact_person': 'John Smith',
                'phone': '555-0101',
                'email': 'contact@medsupply.com',
                'address': '123 Supply Street, Medical District'
            }
        )

        supplier2, _ = Supplier.objects.get_or_create(
            name="PharmaSource Ltd.",
            defaults={
                'contact_person': 'Sarah Johnson',
                'phone': '555-0102',
                'email': 'orders@pharmasource.com',
                'address': '456 Wholesale Ave, Medicine City'
            }
        )

        # Create sample medicines
        medicines_data = [
            {
                'name': 'Paracetamol 500mg',
                'generic_name': 'Acetaminophen',
                'category': 'tablet',
                'manufacturer': 'ABC Pharma',
                'supplier': supplier1,
                'batch_number': 'PAR001',
                'expiry_date': date.today() + timedelta(days=365),
                'purchase_price': Decimal('5.00'),
                'selling_price': Decimal('8.50'),
                'stock_quantity': 100,
                'minimum_stock': 20,
                'description': 'Pain relief and fever reducer'
            },
            {
                'name': 'Amoxicillin 250mg',
                'generic_name': 'Amoxicillin',
                'category': 'capsule',
                'manufacturer': 'XYZ Labs',
                'supplier': supplier2,
                'batch_number': 'AMX001',
                'expiry_date': date.today() + timedelta(days=400),
                'purchase_price': Decimal('12.00'),
                'selling_price': Decimal('18.75'),
                'stock_quantity': 75,
                'minimum_stock': 15,
                'description': 'Antibiotic for bacterial infections'
            },
            {
                'name': 'Cough Syrup 100ml',
                'generic_name': 'Dextromethorphan',
                'category': 'syrup',
                'manufacturer': 'HealthCare Inc',
                'supplier': supplier1,
                'batch_number': 'SYR001',
                'expiry_date': date.today() + timedelta(days=300),
                'purchase_price': Decimal('8.00'),
                'selling_price': Decimal('12.99'),
                'stock_quantity': 50,
                'minimum_stock': 10,
                'description': 'Cough suppressant syrup'
            },
            {
                'name': 'Vitamin D3 1000IU',
                'generic_name': 'Cholecalciferol',
                'category': 'tablet',
                'manufacturer': 'VitaLife',
                'supplier': supplier2,
                'batch_number': 'VIT001',
                'expiry_date': date.today() + timedelta(days=500),
                'purchase_price': Decimal('15.00'),
                'selling_price': Decimal('22.50'),
                'stock_quantity': 5,  # Low stock example
                'minimum_stock': 10,
                'description': 'Vitamin D supplement'
            },
            {
                'name': 'Antiseptic Cream 30g',
                'generic_name': 'Povidone Iodine',
                'category': 'cream',
                'manufacturer': 'SkinCare Ltd',
                'supplier': supplier1,
                'batch_number': 'CRM001',
                'expiry_date': date.today() + timedelta(days=200),
                'purchase_price': Decimal('6.50'),
                'selling_price': Decimal('10.25'),
                'stock_quantity': 30,
                'minimum_stock': 8,
                'description': 'Topical antiseptic cream'
            }
        ]

        for med_data in medicines_data:
            Medicine.objects.get_or_create(
                name=med_data['name'],
                batch_number=med_data['batch_number'],
                defaults=med_data
            )

        # Create sample customers
        customers_data = [
            {
                'name': 'Alice Johnson',
                'phone': '555-1001',
                'email': 'alice@email.com',
                'address': '789 Main St, City'
            },
            {
                'name': 'Bob Williams',
                'phone': '555-1002',
                'email': 'bob@email.com',
                'address': '321 Oak Ave, Town'
            },
            {
                'name': 'Carol Davis',
                'phone': '555-1003',
                'email': 'carol@email.com',
                'address': '654 Pine Rd, Village'
            }
        ]

        for customer_data in customers_data:
            Customer.objects.get_or_create(
                phone=customer_data['phone'],
                defaults=customer_data
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for pharmacy management system')
        )