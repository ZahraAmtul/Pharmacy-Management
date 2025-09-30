from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from pharmacy.models import Supplier, Medicine, Customer, Sale
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Interactive pharmacy management command'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['setup', 'stats', 'cleanup', 'backup'],
            help='Action to perform'
        )

    def handle(self, *args, **options):
        action = options.get('action')
        
        if action == 'setup':
            self.setup_pharmacy()
        elif action == 'stats':
            self.show_statistics()
        elif action == 'cleanup':
            self.cleanup_data()
        elif action == 'backup':
            self.backup_data()
        else:
            self.interactive_menu()

    def interactive_menu(self):
        """Interactive menu for pharmacy management"""
        self.stdout.write(self.style.SUCCESS('\n🏥 PHARMACY MANAGEMENT SYSTEM'))
        self.stdout.write(self.style.SUCCESS('=' * 40))
        
        while True:
            self.stdout.write('\n📋 Choose an option:')
            self.stdout.write('1. 🚀 Quick Setup (Create admin + sample data)')
            self.stdout.write('2. 💊 Populate Medicines')
            self.stdout.write('3. 📊 Show Statistics')
            self.stdout.write('4. 🧹 Cleanup Data')
            self.stdout.write('5. 💾 Backup Data')
            self.stdout.write('6. ❓ Help')
            self.stdout.write('0. 🚪 Exit')
            
            try:
                choice = input('\n👉 Enter your choice (0-6): ').strip()
                
                if choice == '0':
                    self.stdout.write(self.style.SUCCESS('👋 Goodbye!'))
                    break
                elif choice == '1':
                    self.setup_pharmacy()
                elif choice == '2':
                    self.populate_medicines_interactive()
                elif choice == '3':
                    self.show_statistics()
                elif choice == '4':
                    self.cleanup_data()
                elif choice == '5':
                    self.backup_data()
                elif choice == '6':
                    self.show_help()
                else:
                    self.stdout.write(self.style.ERROR('❌ Invalid choice. Please try again.'))
                    
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('\n👋 Goodbye!'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))

    def setup_pharmacy(self):
        """Complete pharmacy setup"""
        self.stdout.write(self.style.SUCCESS('\n🚀 Setting up your pharmacy...'))
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            try:
                User.objects.create_superuser('admin', 'admin@pharmacy.com', 'admin123')
                self.stdout.write(self.style.SUCCESS('👤 Created admin user (admin/admin123)'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating admin: {str(e)}'))
        else:
            self.stdout.write('👤 Admin user already exists')
        
        # Run populate medicines command
        from django.core.management import call_command
        try:
            call_command('populate_medicines', count=100, with_suppliers=True, with_customers=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error populating data: {str(e)}'))

    def populate_medicines_interactive(self):
        """Interactive medicine population"""
        self.stdout.write(self.style.SUCCESS('\n💊 Medicine Population Wizard'))
        self.stdout.write('-' * 30)
        
        try:
            count = input('How many medicines to create? (default: 50): ').strip()
            count = int(count) if count else 50
            
            category = input('Specific category? (tablet/syrup/injection/capsule/cream/drops/other or press Enter for all): ').strip().lower()
            category = category if category in ['tablet', 'syrup', 'injection', 'capsule', 'cream', 'drops', 'other'] else None
            
            clear = input('Clear existing medicines? (y/N): ').strip().lower() == 'y'
            suppliers = input('Create suppliers? (Y/n): ').strip().lower() != 'n'
            customers = input('Create customers? (Y/n): ').strip().lower() != 'n'
            
            # Build command arguments
            from django.core.management import call_command
            kwargs = {
                'count': count,
                'clear': clear,
                'with_suppliers': suppliers,
                'with_customers': customers
            }
            if category:
                kwargs['category'] = category
                
            call_command('populate_medicines', **kwargs)
            
        except ValueError:
            self.stdout.write(self.style.ERROR('❌ Invalid number entered'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⏹️  Operation cancelled'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))

    def show_statistics(self):
        """Show comprehensive pharmacy statistics"""
        self.stdout.write(self.style.SUCCESS('\n📊 PHARMACY STATISTICS'))
        self.stdout.write('=' * 40)
        
        # Medicine statistics
        total_medicines = Medicine.objects.count()
        self.stdout.write(f'💊 Total Medicines: {total_medicines}')
        
        if total_medicines > 0:
            # Category breakdown
            self.stdout.write('\n📋 By Category:')
            for category_code, category_name in Medicine.CATEGORY_CHOICES:
                count = Medicine.objects.filter(category=category_code).count()
                if count > 0:
                    percentage = (count / total_medicines) * 100
                    self.stdout.write(f'   • {category_name}: {count} ({percentage:.1f}%)')
            
            # Stock alerts
            low_stock = Medicine.objects.filter(stock_quantity__lte=models.F('minimum_stock')).count()
            expired = Medicine.objects.filter(expiry_date__lt=date.today()).count()
            expiring_soon = Medicine.objects.filter(
                expiry_date__gte=date.today(),
                expiry_date__lte=date.today() + timedelta(days=30)
            ).count()
            
            self.stdout.write(f'\n⚠️  Stock Alerts:')
            self.stdout.write(f'   • Low Stock: {low_stock}')
            self.stdout.write(f'   • Expired: {expired}')
            self.stdout.write(f'   • Expiring Soon (30 days): {expiring_soon}')
            
            # Value statistics
            total_value = sum(med.selling_price * med.stock_quantity for med in Medicine.objects.all())
            self.stdout.write(f'\n💰 Total Inventory Value: ${total_value:,.2f}')
        
        # Other statistics
        total_suppliers = Supplier.objects.count()
        total_customers = Customer.objects.count()
        total_sales = Sale.objects.count()
        
        self.stdout.write(f'\n🏢 Total Suppliers: {total_suppliers}')
        self.stdout.write(f'👥 Total Customers: {total_customers}')
        self.stdout.write(f'🛒 Total Sales: {total_sales}')
        
        if total_sales > 0:
            total_revenue = sum(sale.final_amount for sale in Sale.objects.all())
            self.stdout.write(f'💵 Total Revenue: ${total_revenue:,.2f}')

    def cleanup_data(self):
        """Interactive data cleanup"""
        self.stdout.write(self.style.WARNING('\n🧹 DATA CLEANUP'))
        self.stdout.write('-' * 20)
        
        try:
            self.stdout.write('⚠️  WARNING: This will permanently delete data!')
            confirm = input('Are you sure you want to continue? (type "yes" to confirm): ').strip()
            
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.SUCCESS('✅ Operation cancelled'))
                return
            
            self.stdout.write('\nWhat would you like to clean up?')
            self.stdout.write('1. Expired medicines only')
            self.stdout.write('2. All medicines')
            self.stdout.write('3. All customers')
            self.stdout.write('4. All sales history')
            self.stdout.write('5. Everything (complete reset)')
            
            choice = input('Enter choice (1-5): ').strip()
            
            if choice == '1':
                deleted = Medicine.objects.filter(expiry_date__lt=date.today()).delete()
                self.stdout.write(self.style.SUCCESS(f'🗑️  Deleted {deleted[0]} expired medicines'))
            elif choice == '2':
                deleted = Medicine.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'🗑️  Deleted {deleted[0]} medicines'))
            elif choice == '3':
                deleted = Customer.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'🗑️  Deleted {deleted[0]} customers'))
            elif choice == '4':
                deleted = Sale.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'🗑️  Deleted {deleted[0]} sales records'))
            elif choice == '5':
                Medicine.objects.all().delete()
                Customer.objects.all().delete()
                Sale.objects.all().delete()
                Supplier.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('🗑️  Complete database cleanup done'))
            else:
                self.stdout.write(self.style.ERROR('❌ Invalid choice'))
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⏹️  Operation cancelled'))

    def backup_data(self):
        """Create data backup"""
        self.stdout.write(self.style.SUCCESS('\n💾 Creating backup...'))
        
        try:
            from django.core.management import call_command
            from datetime import datetime
            
            backup_file = f'pharmacy_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            with open(backup_file, 'w') as f:
                call_command('dumpdata', 'pharmacy', stdout=f)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Backup created: {backup_file}'))
            self.stdout.write('To restore: python manage.py loaddata {}'.format(backup_file))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Backup failed: {str(e)}'))

    def show_help(self):
        """Show help information"""
        self.stdout.write(self.style.SUCCESS('\n❓ HELP - Command Usage'))
        self.stdout.write('=' * 40)
        self.stdout.write('\n🚀 Quick Commands:')
        self.stdout.write('python manage.py populate_medicines --count 100 --with-suppliers --with-customers')
        self.stdout.write('python manage.py populate_medicines --category tablet --count 50')
        self.stdout.write('python manage.py populate_medicines --clear --count 200')
        self.stdout.write('\npython manage.py manage_pharmacy --action setup')
        self.stdout.write('python manage.py manage_pharmacy --action stats')
        self.stdout.write('python manage.py manage_pharmacy --action cleanup')
        
        self.stdout.write('\n📚 Available Categories:')
        for code, name in Medicine.CATEGORY_CHOICES:
            self.stdout.write(f'   • {code}: {name}')
        
        self.stdout.write('\n🎯 Tips:')
        self.stdout.write('• Use --clear to reset data before populating')
        self.stdout.write('• Create suppliers first for better organization')
        self.stdout.write('• Start with setup command for first-time use')
        self.stdout.write('• Regular backups are recommended')