from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('search-medicine/', views.search_medicine, name='search_medicine'),
    path('create-sale/', views.create_sale, name='create_sale'),
    path('receipt/<int:sale_id>/', views.print_receipt, name='print_receipt'),
    path('sales-history/', views.sales_history, name='sales_history'),
    path('api/medicine/<int:medicine_id>/', views.get_medicine_details, name='medicine_details'),
]