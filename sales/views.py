from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Customer, Order, Invoice
from .forms import CustomerForm, OrderForm, InvoiceForm
from erp_project.export_import_utils import export_to_csv, export_to_pdf, import_from_csv

# Dashboard View
def dashboard(request):
    customers_count = Customer.objects.count()
    orders_count = Order.objects.count()
    invoices_count = Invoice.objects.count()
    return render(request, 'sales/dashboard.html', {
        'customers_count': customers_count,
        'orders_count': orders_count,
        'invoices_count': invoices_count
    })

# Customer Views
def customers_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customers.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'sales/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customers_list')

# Order Views
def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'sales/orders.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'sales/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'sales/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('orders_list')

# Invoice Views
def invoices_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'sales/invoices.html', {'invoices': invoices})

def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoices_list')
    else:
        form = InvoiceForm()
    return render(request, 'sales/invoice_form.html', {'form': form})

def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoices_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'sales/invoice_form.html', {'form': form})

def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('invoices_list')

# Export/Import Views for Sales

def export_customers(request, format_type='csv'):
    fields = ['id', 'name', 'email', 'phone', 'address', 'created_at']
    customers = Customer.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('customers', customers, fields, 'Customers List')
    else:
        return export_to_csv('customers', customers, fields)

def export_orders(request, format_type='csv'):
    fields = ['id', 'customer__name', 'order_date', 'total_amount', 'status', 'created_at']
    orders = Order.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('orders', orders, fields, 'Orders List')
    else:
        return export_to_csv('orders', orders, fields)

def export_invoices(request, format_type='csv'):
    fields = ['id', 'order__customer__name', 'invoice_date', 'amount', 'status', 'created_at']
    invoices = Invoice.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('invoices', invoices, fields, 'Invoices List')
    else:
        return export_to_csv('invoices', invoices, fields)

@require_http_methods(["POST"])
def import_customers(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('sales:customers_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Phone': 'phone',
        'Address': 'address'
    }
    
    success, message = import_from_csv(Customer, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('sales:customers_list')

@require_http_methods(["POST"])
def import_orders(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('sales:orders_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Customer': 'customer',
        'Order Date': 'order_date',
        'Total Amount': 'total_amount',
        'Status': 'status'
    }
    
    success, message = import_from_csv(Order, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('sales:orders_list')

@require_http_methods(["POST"])
def import_invoices(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('sales:invoices_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Order': 'order',
        'Invoice Date': 'invoice_date',
        'Amount': 'amount',
        'Status': 'status'
    }
    
    success, message = import_from_csv(Invoice, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('sales:invoices_list')
