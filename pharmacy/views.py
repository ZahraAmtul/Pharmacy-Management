from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from decimal import Decimal
import json

from .models import Medicine, Customer, Sale, SaleItem, Supplier
from .forms import MedicineForm, CustomerForm, SaleForm, SupplierForm, MedicineSearchForm

@login_required
def dashboard(request):
    # Statistics for dashboard
    total_medicines = Medicine.objects.count()
    low_stock_count = Medicine.objects.filter(stock_quantity__lte=models.F('minimum_stock')).count()
    expired_count = Medicine.objects.filter(expiry_date__lt=timezone.now().date()).count()
    today_sales = Sale.objects.filter(created_at__date=timezone.now().date()).count()
    today_revenue = Sale.objects.filter(
        created_at__date=timezone.now().date()
    ).aggregate(total=Sum('final_amount'))['total'] or 0

    low_stock_medicines = Medicine.objects.filter(
        stock_quantity__lte=models.F('minimum_stock')
    )[:5]
    
    recent_sales = Sale.objects.order_by('-created_at')[:5]

    context = {
        'total_medicines': total_medicines,
        'low_stock_count': low_stock_count,
        'expired_count': expired_count,
        'today_sales': today_sales,
        'today_revenue': today_revenue,
        'low_stock_medicines': low_stock_medicines,
        'recent_sales': recent_sales,
    }
    return render(request, 'pharmacy/dashboard.html', context)

@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine added successfully!')
            return redirect('pharmacy:add_medicine')
    else:
        form = MedicineForm()
    
    return render(request, 'pharmacy/add_medicine.html', {'form': form})

@login_required
def search_medicine(request):
    form = MedicineSearchForm()
    medicines = Medicine.objects.all()
    
    if request.GET.get('query'):
        query = request.GET.get('query')
        medicines = medicines.filter(
            Q(name__icontains=query) |
            Q(generic_name__icontains=query) |
            Q(manufacturer__icontains=query)
        )
    
    if request.GET.get('category'):
        category = request.GET.get('category')
        medicines = medicines.filter(category=category)
    
    context = {
        'form': form,
        'medicines': medicines,
        'query': request.GET.get('query', ''),
        'selected_category': request.GET.get('category', ''),
    }
    return render(request, 'pharmacy/search_medicine.html', context)

@login_required
def create_sale(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            customer_id = data.get('customer_id')
            discount = Decimal(str(data.get('discount', 0)))
            tax = Decimal(str(data.get('tax', 0)))
            payment_method = data.get('payment_method', 'cash')

            if not items:
                return JsonResponse({'success': False, 'error': 'No items in cart'})

            # Calculate total
            total_amount = Decimal('0')
            for item in items:
                total_amount += Decimal(str(item['total']))

            # Calculate final amount
            discount_amount = (total_amount * discount) / 100
            tax_amount = ((total_amount - discount_amount) * tax) / 100
            final_amount = total_amount - discount_amount + tax_amount

            # Create sale
            customer = None
            if customer_id:
                customer = Customer.objects.get(id=customer_id)

            sale = Sale.objects.create(
                customer=customer,
                cashier=request.user,
                total_amount=total_amount,
                discount=discount,
                tax=tax,
                final_amount=final_amount,
                payment_method=payment_method
            )

            # Create sale items
            for item in items:
                medicine = Medicine.objects.get(id=item['medicine_id'])
                SaleItem.objects.create(
                    sale=sale,
                    medicine=medicine,
                    quantity=item['quantity'],
                    unit_price=Decimal(str(item['price'])),
                    total_price=Decimal(str(item['total']))
                )

            return JsonResponse({
                'success': True,
                'sale_id': sale.id,
                'message': 'Sale completed successfully!'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # GET request - show create sale page
    customers = Customer.objects.all()
    medicines = Medicine.objects.filter(stock_quantity__gt=0)
    
    context = {
        'customers': customers,
        'medicines': medicines,
    }
    return render(request, 'pharmacy/create_sale.html', context)

@login_required
def print_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    context = {'sale': sale}
    return render(request, 'pharmacy/receipt.html', context)

@login_required
def sales_history(request):
    sales = Sale.objects.order_by('-created_at')
    return render(request, 'pharmacy/sales_history.html', {'sales': sales})

@login_required
def get_medicine_details(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    data = {
        'id': medicine.id,
        'name': medicine.name,
        'price': str(medicine.selling_price),
        'stock': medicine.stock_quantity,
    }
    return JsonResponse(data)