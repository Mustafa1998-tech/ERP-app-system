from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import pandas as pd
import json
from datetime import datetime

from .models import Product, Supplier, PurchaseOrder
from .forms import ProductForm, SupplierForm, PurchaseOrderForm

# Product Views
def products_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/products.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:products_list')  # Updated to use namespace
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('products_list')

def product_detail(request, pk):
    """View to display detailed information about a specific product."""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'title': f'Product: {product.name}'
    }
    return render(request, 'inventory/product_detail.html', context)

def export_products_csv(request):
    """Export products to CSV"""
    # Get all products
    products = Product.objects.all().values('sku', 'name', 'description', 'price', 'quantity', 'category__name', 'supplier__name')
    
    # Convert to DataFrame
    df = pd.DataFrame(list(products))
    
    # Rename columns for better readability
    df = df.rename(columns={
        'category__name': 'category',
        'supplier__name': 'supplier'
    })
    
    # Create response with CSV data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_export_{}.csv"'.format(
        timezone.now().strftime('%Y%m%d_%H%M%S')
    )
    
    # Write DataFrame to response
    df.to_csv(response, index=False)
    return response

def export_products_pdf(request):
    """Export products to PDF"""
    # Get all products
    products = Product.objects.select_related('category', 'supplier').all()
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products_export_{}.pdf"'.format(
        timezone.now().strftime('%Y%m%d_%H%M%S')
    )
    
    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1  # Center
    )
    title = Paragraph("Products Export - {}".format(timezone.now().strftime('%Y-%m-%d %H:%M')), title_style)
    elements.append(title)
    
    # Prepare data for the table
    data = [['SKU', 'Name', 'Category', 'Supplier', 'Price', 'Qty']]
    
    for product in products:
        data.append([
            product.sku,
            product.name,
            str(product.category) if product.category else '',
            str(product.supplier) if product.supplier else '',
            f"${product.price:.2f}",
            str(product.quantity)
        ])
    
    # Create the table
    table = Table(data, colWidths=[1*inch, 2*inch, 1.5*inch, 1.5*inch, 0.75*inch, 0.5*inch])
    
    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),  # Right align price and quantity
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    # Apply the style to the table
    table.setStyle(style)
    
    # Add the table to the elements
    elements.append(table)
    
    # Add footer
    elements.append(Spacer(1, 12))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=2  # Right
    )
    footer = Paragraph("Generated on {}".format(timezone.now().strftime('%Y-%m-%d %H:%M')), footer_style)
    elements.append(footer)
    
    # Build the PDF
    doc.build(elements)
    
    return response

@require_http_methods(["POST"])
def import_products(request):
    """Import products from CSV or PDF"""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    file_extension = file.name.split('.')[-1].lower()
    
    try:
        if file_extension == 'csv':
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Basic validation
            required_columns = ['sku', 'name', 'price', 'quantity']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return JsonResponse(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'}, 
                    status=400
                )
            
            # Process each row
            created_count = 0
            updated_count = 0
            
            with transaction.atomic():
                for _, row in df.iterrows():
                    # Check if product exists
                    product, created = Product.objects.update_or_create(
                        sku=row['sku'],
                        defaults={
                            'name': row['name'],
                            'description': row.get('description', ''),
                            'price': float(row['price']),
                            'quantity': int(row['quantity']),
                            # Add other fields as needed
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully imported {created_count} new products and updated {updated_count} existing products.'
            })
            
        elif file_extension == 'pdf':
            # For PDF import, we'll just return a message since PDF parsing is complex
            # In a real application, you would use a PDF parsing library like PyPDF2 or pdfplumber
            return JsonResponse({
                'error': 'PDF import is not yet implemented. Please use CSV format for now.'
            }, status=400)
            
        else:
            return JsonResponse(
                {'error': 'Unsupported file format. Please upload a CSV or PDF file.'}, 
                status=400
            )
            
    except Exception as e:
        return JsonResponse(
            {'error': f'Error processing file: {str(e)}'}, 
            status=400
        )

# Supplier Views
def suppliers_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/suppliers.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('suppliers_list')

# Purchase Order Views
def purchase_orders_list(request):
    purchase_orders = PurchaseOrder.objects.all()
    return render(request, 'inventory/purchase_orders.html', {'purchase_orders': purchase_orders})

def purchase_order_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_orders_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'inventory/purchase_order_form.html', {'form': form})

def purchase_order_update(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        if form.is_valid():
            form.save()
            return redirect('purchase_orders_list')
    else:
        form = PurchaseOrderForm(instance=purchase_order)
    return render(request, 'inventory/purchase_order_form.html', {'form': form})

def purchase_order_delete(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    purchase_order.delete()
    return redirect('purchase_orders_list')
