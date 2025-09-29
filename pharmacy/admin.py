from django.contrib import admin
from .models import Supplier, Medicine, Customer, Sale, SaleItem

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'created_at']
    search_fields = ['name', 'contact_person', 'phone']
    list_filter = ['created_at']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'manufacturer', 'batch_number', 'stock_quantity', 'selling_price', 'expiry_date', 'is_low_stock']
    search_fields = ['name', 'generic_name', 'manufacturer', 'batch_number']
    list_filter = ['category', 'manufacturer', 'supplier', 'expiry_date']
    list_editable = ['stock_quantity', 'selling_price']
    ordering = ['name']
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'cashier', 'final_amount', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'created_at', 'cashier']
    search_fields = ['customer__name', 'customer__phone']
    inlines = [SaleItemInline]
    readonly_fields = ['created_at']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'medicine', 'quantity', 'unit_price', 'total_price']
    list_filter = ['sale__created_at']
    search_fields = ['medicine__name', 'sale__id']