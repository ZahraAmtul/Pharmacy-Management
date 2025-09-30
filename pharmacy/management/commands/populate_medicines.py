from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from pharmacy.models import Supplier, Medicine, Customer
from datetime import date, timedelta
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate pharmacy database with realistic medicine data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of medicines to create (default: 50)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing medicine data before populating'
        )
        parser.add_argument(
            '--with-suppliers',
            action='store_true',
            help='Create suppliers if they don\'t exist'
        )
        parser.add_argument(
            '--with-customers',
            action='store_true',
            help='Create sample customers'
        )
        parser.add_argument(
            '--category',
            type=str,
            choices=['tablet', 'syrup', 'injection', 'capsule', 'cream', 'drops', 'other'],
            help='Only create medicines of specific category'
        )

    def handle(self, *args, **options):
        count = options['count']
        clear_data = options['clear']
        create_suppliers = options['with_suppliers']
        create_customers = options['with_customers']
        specific_category = options['category']

        self.stdout.write(self.style.SUCCESS(f'🏥 Starting Pharmacy Data Population...'))

        # Clear existing data if requested
        if clear_data:
            self.stdout.write('🗑️  Clearing existing medicine data...')
            Medicine.objects.all().delete()
            if create_suppliers:
                Supplier.objects.all().delete()
            if create_customers:
                Customer.objects.all().delete()

        # Create or get suppliers
        suppliers = self.create_suppliers() if create_suppliers else self.get_or_create_default_suppliers()
        
        # Create customers if requested
        if create_customers:
            self.create_customers()

        # Create medicines
        self.create_medicines(count, suppliers, specific_category)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully populated pharmacy with {count} medicines!')
        )

    def get_or_create_default_suppliers(self):
        """Get existing suppliers or create default ones"""
        suppliers = list(Supplier.objects.all())
        if not suppliers:
            suppliers = self.create_suppliers()
        return suppliers

    def create_suppliers(self):
        """Create realistic pharmaceutical suppliers"""
        suppliers_data = [
            {
                'name': 'MediCore Pharmaceuticals',
                'contact_person': 'Dr. Sarah Johnson',
                'phone': '555-0101',
                'email': 'orders@medicore.com',
                'address': '123 Pharma Street, Medical District, NY 10001'
            },
            {
                'name': 'HealthPlus Supply Co.',
                'contact_person': 'Michael Chen',
                'phone': '555-0102',
                'email': 'supply@healthplus.com',
                'address': '456 Medicine Ave, Healthcare City, CA 90210'
            },
            {
                'name': 'Global Drug Distribution',
                'contact_person': 'Emily Rodriguez',
                'phone': '555-0103',
                'email': 'info@globaldrug.com',
                'address': '789 Distribution Blvd, Supply Town, TX 75001'
            },
            {
                'name': 'Premium Medical Supplies',
                'contact_person': 'James Wilson',
                'phone': '555-0104',
                'email': 'contact@premiummed.com',
                'address': '321 Quality Road, Excellence City, FL 33101'
            },
            {
                'name': 'UniPharma International',
                'contact_person': 'Dr. Lisa Thompson',
                'phone': '555-0105',
                'email': 'sales@unipharma.com',
                'address': '654 Global Plaza, International District, WA 98001'
            }
        ]

        suppliers = []
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults=supplier_data
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(f'📦 Created supplier: {supplier.name}')

        return suppliers

    def create_customers(self):
        """Create sample customers"""
        customers_data = [
            {'name': 'Alice Johnson', 'phone': '555-1001', 'email': 'alice@email.com', 'address': '123 Main St, City'},
            {'name': 'Bob Williams', 'phone': '555-1002', 'email': 'bob@email.com', 'address': '456 Oak Ave, Town'},
            {'name': 'Carol Davis', 'phone': '555-1003', 'email': 'carol@email.com', 'address': '789 Pine Rd, Village'},
            {'name': 'David Brown', 'phone': '555-1004', 'email': 'david@email.com', 'address': '321 Elm St, Borough'},
            {'name': 'Emma Wilson', 'phone': '555-1005', 'email': 'emma@email.com', 'address': '654 Cedar Ln, Township'},
            {'name': 'Frank Miller', 'phone': '555-1006', 'email': 'frank@email.com', 'address': '987 Birch Dr, Suburb'},
            {'name': 'Grace Lee', 'phone': '555-1007', 'email': 'grace@email.com', 'address': '147 Maple Ave, District'},
            {'name': 'Henry Garcia', 'phone': '555-1008', 'email': 'henry@email.com', 'address': '258 Spruce St, Area'},
        ]

        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                phone=customer_data['phone'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'👤 Created customer: {customer.name}')

    def create_medicines(self, count, suppliers, specific_category=None):
        """Create realistic medicines data"""
        
        # Comprehensive medicine database
        medicines_database = {
            'tablet': [
                # Pain Relief & Fever
                {'name': 'Paracetamol 500mg', 'generic': 'Acetaminophen', 'manufacturer': 'PharmaCorp', 'desc': 'Pain relief and fever reducer'},
                {'name': 'Ibuprofen 400mg', 'generic': 'Ibuprofen', 'manufacturer': 'MediLabs', 'desc': 'Anti-inflammatory pain reliever'},
                {'name': 'Aspirin 325mg', 'generic': 'Acetylsalicylic Acid', 'manufacturer': 'HealthCare Inc', 'desc': 'Pain relief and blood thinner'},
                {'name': 'Naproxen 220mg', 'generic': 'Naproxen Sodium', 'manufacturer': 'WellMed', 'desc': 'Long-lasting pain relief'},
                
                # Antibiotics
                {'name': 'Azithromycin 250mg', 'generic': 'Azithromycin', 'manufacturer': 'BioPharm', 'desc': 'Antibiotic for bacterial infections'},
                {'name': 'Ciprofloxacin 500mg', 'generic': 'Ciprofloxacin', 'manufacturer': 'MediCore', 'desc': 'Broad-spectrum antibiotic'},
                {'name': 'Doxycycline 100mg', 'generic': 'Doxycycline', 'manufacturer': 'PharmaTech', 'desc': 'Tetracycline antibiotic'},
                
                # Cardiovascular
                {'name': 'Lisinopril 10mg', 'generic': 'Lisinopril', 'manufacturer': 'CardioMed', 'desc': 'ACE inhibitor for blood pressure'},
                {'name': 'Metoprolol 50mg', 'generic': 'Metoprolol', 'manufacturer': 'HeartCare', 'desc': 'Beta-blocker for heart conditions'},
                {'name': 'Amlodipine 5mg', 'generic': 'Amlodipine', 'manufacturer': 'VascuPharm', 'desc': 'Calcium channel blocker'},
                
                # Diabetes
                {'name': 'Metformin 500mg', 'generic': 'Metformin HCl', 'manufacturer': 'DiabeCare', 'desc': 'Type 2 diabetes medication'},
                {'name': 'Glipizide 5mg', 'generic': 'Glipizide', 'manufacturer': 'EndoPharm', 'desc': 'Blood sugar control medication'},
                
                # Mental Health
                {'name': 'Sertraline 50mg', 'generic': 'Sertraline HCl', 'manufacturer': 'MindWell', 'desc': 'Antidepressant medication'},
                {'name': 'Lorazepam 1mg', 'generic': 'Lorazepam', 'manufacturer': 'CalmCare', 'desc': 'Anti-anxiety medication'},
                
                # Vitamins & Supplements
                {'name': 'Vitamin D3 1000IU', 'generic': 'Cholecalciferol', 'manufacturer': 'VitaLife', 'desc': 'Bone health supplement'},
                {'name': 'Vitamin B12 500mcg', 'generic': 'Cyanocobalamin', 'manufacturer': 'NutriHealth', 'desc': 'Energy and nerve health'},
                {'name': 'Multivitamin Daily', 'generic': 'Multiple Vitamins', 'manufacturer': 'WellVit', 'desc': 'Complete daily nutrition'},
                {'name': 'Calcium 600mg', 'generic': 'Calcium Carbonate', 'manufacturer': 'BoneStrong', 'desc': 'Bone and teeth health'},
                {'name': 'Iron 65mg', 'generic': 'Ferrous Sulfate', 'manufacturer': 'BloodHealth', 'desc': 'Iron deficiency supplement'},
                
                # Allergy & Cold
                {'name': 'Cetirizine 10mg', 'generic': 'Cetirizine HCl', 'manufacturer': 'AllergyFree', 'desc': 'Antihistamine for allergies'},
                {'name': 'Loratadine 10mg', 'generic': 'Loratadine', 'manufacturer': 'ClearAir', 'desc': 'Non-drowsy allergy relief'},
                {'name': 'Pseudoephedrine 30mg', 'generic': 'Pseudoephedrine', 'manufacturer': 'DecongestCare', 'desc': 'Nasal decongestant'},
            ],
            
            'capsule': [
                {'name': 'Amoxicillin 250mg', 'generic': 'Amoxicillin', 'manufacturer': 'AntiBio Labs', 'desc': 'Penicillin antibiotic'},
                {'name': 'Omeprazole 20mg', 'generic': 'Omeprazole', 'manufacturer': 'GastroMed', 'desc': 'Proton pump inhibitor'},
                {'name': 'Fluoxetine 20mg', 'generic': 'Fluoxetine HCl', 'manufacturer': 'MentalHealth Pro', 'desc': 'SSRI antidepressant'},
                {'name': 'Gabapentin 300mg', 'generic': 'Gabapentin', 'manufacturer': 'NeuroCare', 'desc': 'Nerve pain medication'},
                {'name': 'Pregabalin 75mg', 'generic': 'Pregabalin', 'manufacturer': 'PainRelief Inc', 'desc': 'Neuropathic pain treatment'},
                {'name': 'Fish Oil 1000mg', 'generic': 'Omega-3 Fatty Acids', 'manufacturer': 'OceanHealth', 'desc': 'Heart and brain health'},
                {'name': 'Probiotic Complex', 'generic': 'Lactobacillus Mix', 'manufacturer': 'GutHealth', 'desc': 'Digestive health support'},
                {'name': 'Turmeric 500mg', 'generic': 'Curcumin Extract', 'manufacturer': 'HerbalWell', 'desc': 'Anti-inflammatory supplement'},
            ],
            
            'syrup': [
                {'name': 'Cough Syrup 100ml', 'generic': 'Dextromethorphan', 'manufacturer': 'CoughCare', 'desc': 'Cough suppressant'},
                {'name': 'Paediatric Fever Syrup', 'generic': 'Paracetamol', 'manufacturer': 'KidsHealth', 'desc': 'Children\'s fever reducer'},
                {'name': 'Antacid Syrup 200ml', 'generic': 'Aluminum Hydroxide', 'manufacturer': 'TummyEase', 'desc': 'Acid reflux relief'},
                {'name': 'Iron Tonic 200ml', 'generic': 'Ferrous Gluconate', 'manufacturer': 'BloodBoost', 'desc': 'Iron deficiency treatment'},
                {'name': 'Vitamin C Syrup', 'generic': 'Ascorbic Acid', 'manufacturer': 'ImmuneBoost', 'desc': 'Immune system support'},
                {'name': 'Expectorant Syrup', 'generic': 'Guaifenesin', 'manufacturer': 'ChestClear', 'desc': 'Mucus relief medication'},
                {'name': 'Multivitamin Syrup', 'generic': 'Multiple Vitamins', 'manufacturer': 'ChildVitals', 'desc': 'Children\'s nutrition support'},
            ],
            
            'injection': [
                {'name': 'Insulin Rapid 10ml', 'generic': 'Insulin Aspart', 'manufacturer': 'DiabetesControl', 'desc': 'Fast-acting insulin'},
                {'name': 'Vitamin B12 Injection', 'generic': 'Cyanocobalamin', 'manufacturer': 'VitaShot', 'desc': 'B12 deficiency treatment'},
                {'name': 'Tetanus Vaccine', 'generic': 'Tetanus Toxoid', 'manufacturer': 'ImmunePro', 'desc': 'Tetanus prevention vaccine'},
                {'name': 'Morphine 10mg/ml', 'generic': 'Morphine Sulfate', 'manufacturer': 'PainControl', 'desc': 'Severe pain management'},
                {'name': 'Epinephrine Auto-injector', 'generic': 'Epinephrine', 'manufacturer': 'EmergencyCare', 'desc': 'Severe allergic reaction treatment'},
                {'name': 'Antibiotic Injection', 'generic': 'Ceftriaxone', 'manufacturer': 'InfectionFight', 'desc': 'Serious bacterial infections'},
            ],
            
            'cream': [
                {'name': 'Antiseptic Cream 30g', 'generic': 'Povidone Iodine', 'manufacturer': 'WoundCare', 'desc': 'Topical antiseptic'},
                {'name': 'Hydrocortisone Cream 1%', 'generic': 'Hydrocortisone', 'manufacturer': 'SkinRelief', 'desc': 'Anti-inflammatory skin cream'},
                {'name': 'Antifungal Cream 15g', 'generic': 'Clotrimazole', 'manufacturer': 'FungusAway', 'desc': 'Fungal infection treatment'},
                {'name': 'Moisturizing Cream 50g', 'generic': 'Urea 10%', 'manufacturer': 'SkinSoft', 'desc': 'Dry skin treatment'},
                {'name': 'Acne Treatment Gel', 'generic': 'Benzoyl Peroxide', 'manufacturer': 'ClearSkin', 'desc': 'Acne medication'},
                {'name': 'Pain Relief Gel 30g', 'generic': 'Diclofenac', 'manufacturer': 'TopicalPain', 'desc': 'Topical pain relief'},
                {'name': 'Eczema Cream 25g', 'generic': 'Tacrolimus', 'manufacturer': 'DermaHealth', 'desc': 'Eczema treatment'},
            ],
            
            'drops': [
                {'name': 'Eye Drops 10ml', 'generic': 'Artificial Tears', 'manufacturer': 'EyeCare Plus', 'desc': 'Dry eye relief'},
                {'name': 'Antibiotic Eye Drops', 'generic': 'Chloramphenicol', 'manufacturer': 'VisionClear', 'desc': 'Eye infection treatment'},
                {'name': 'Ear Drops 15ml', 'generic': 'Hydrogen Peroxide', 'manufacturer': 'HearWell', 'desc': 'Ear wax removal'},
                {'name': 'Nasal Drops 10ml', 'generic': 'Saline Solution', 'manufacturer': 'BreathEasy', 'desc': 'Nasal congestion relief'},
                {'name': 'Glaucoma Drops', 'generic': 'Timolol', 'manufacturer': 'EyePressure', 'desc': 'Glaucoma treatment'},
                {'name': 'Allergy Eye Drops', 'generic': 'Ketotifen', 'manufacturer': 'AllergyEye', 'desc': 'Allergic conjunctivitis relief'},
            ],
            
            'other': [
                {'name': 'Adhesive Bandages', 'generic': 'Sterile Bandages', 'manufacturer': 'FirstAid Pro', 'desc': 'Wound protection'},
                {'name': 'Thermometer Digital', 'generic': 'Digital Thermometer', 'manufacturer': 'HealthTech', 'desc': 'Body temperature measurement'},
                {'name': 'Blood Pressure Monitor', 'generic': 'BP Monitor', 'manufacturer': 'CardioCheck', 'desc': 'Blood pressure monitoring'},
                {'name': 'Glucose Test Strips', 'generic': 'Glucose Strips', 'manufacturer': 'DiabetesTest', 'desc': 'Blood sugar testing'},
                {'name': 'Surgical Mask Box', 'generic': 'Disposable Masks', 'manufacturer': 'SafetyFirst', 'desc': 'Protective face masks'},
                {'name': 'Hand Sanitizer 250ml', 'generic': 'Alcohol-based Sanitizer', 'manufacturer': 'CleanHands', 'desc': 'Hand disinfection'},
                {'name': 'Pregnancy Test Kit', 'generic': 'hCG Test', 'manufacturer': 'BabyCheck', 'desc': 'Pregnancy detection'},
            ]
        }

        # Filter by category if specified
        if specific_category:
            if specific_category in medicines_database:
                available_medicines = {specific_category: medicines_database[specific_category]}
            else:
                self.stdout.write(self.style.ERROR(f'Category "{specific_category}" not found!'))
                return
        else:
            available_medicines = medicines_database

        created_count = 0
        for category, medicines_list in available_medicines.items():
            category_count = 0
            target_per_category = count // len(available_medicines) if not specific_category else count
            
            for medicine_data in medicines_list:
                if category_count >= target_per_category and not specific_category:
                    break
                
                # Generate random data
                supplier = random.choice(suppliers)
                batch_number = f"{medicine_data['name'][:3].upper()}{random.randint(1000, 9999)}"
                
                # Price ranges based on category
                price_ranges = {
                    'tablet': (2.00, 25.00),
                    'capsule': (5.00, 40.00),
                    'syrup': (8.00, 35.00),
                    'injection': (15.00, 150.00),
                    'cream': (6.00, 30.00),
                    'drops': (10.00, 45.00),
                    'other': (3.00, 200.00)
                }
                
                min_price, max_price = price_ranges.get(category, (5.00, 30.00))
                purchase_price = Decimal(str(round(random.uniform(min_price * 0.6, min_price * 0.8), 2)))
                selling_price = Decimal(str(round(random.uniform(min_price, max_price), 2)))
                
                # Stock quantities
                stock_quantity = random.randint(10, 200)
                minimum_stock = random.randint(5, 20)
                
                # Expiry dates (6 months to 3 years from now)
                expiry_days = random.randint(180, 1095)
                expiry_date = date.today() + timedelta(days=expiry_days)
                
                # Create medicine
                medicine, created = Medicine.objects.get_or_create(
                    name=medicine_data['name'],
                    batch_number=batch_number,
                    defaults={
                        'generic_name': medicine_data['generic'],
                        'category': category,
                        'manufacturer': medicine_data['manufacturer'],
                        'supplier': supplier,
                        'expiry_date': expiry_date,
                        'purchase_price': purchase_price,
                        'selling_price': selling_price,
                        'stock_quantity': stock_quantity,
                        'minimum_stock': minimum_stock,
                        'description': medicine_data['desc']
                    }
                )
                
                if created:
                    created_count += 1
                    category_count += 1
                    if created_count % 10 == 0:
                        self.stdout.write(f'💊 Created {created_count} medicines...')
                
                if created_count >= count:
                    break
            
            if created_count >= count:
                break

        self.stdout.write(
            self.style.SUCCESS(f'🎉 Created {created_count} medicines successfully!')
        )
        
        # Show summary
        self.show_summary()

    def show_summary(self):
        """Display a summary of current data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 PHARMACY DATABASE SUMMARY'))
        self.stdout.write('='*50)
        
        # Medicine statistics
        total_medicines = Medicine.objects.count()
        categories_stats = {}
        for category_code, category_name in Medicine.CATEGORY_CHOICES:
            count = Medicine.objects.filter(category=category_code).count()
            if count > 0:
                categories_stats[category_name] = count
        
        self.stdout.write(f'💊 Total Medicines: {total_medicines}')
        self.stdout.write('📋 By Category:')
        for category, count in categories_stats.items():
            self.stdout.write(f'   • {category}: {count}')
        
        # Stock alerts
        low_stock = Medicine.objects.filter(stock_quantity__lte = models.F('minimum_stock')).count()
        expired = Medicine.objects.filter(expiry_date__lt=date.today()).count()
        
        self.stdout.write(f'⚠️  Low Stock Items: {low_stock}')
        self.stdout.write(f'❌ Expired Items: {expired}')
        
        # Other statistics
        total_suppliers = Supplier.objects.count()
        total_customers = Customer.objects.count()
        
        self.stdout.write(f'🏢 Total Suppliers: {total_suppliers}')
        self.stdout.write(f'👥 Total Customers: {total_customers}')
        
        self.stdout.write('='*50)
        self.stdout.write(self.style.SUCCESS('✅ Database population complete!'))
        self.stdout.write('='*50 + '\n')