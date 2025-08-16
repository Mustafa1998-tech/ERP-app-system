from django.urls import path
from . import views

app_name = 'inventory'  # Add this line for namespace support

urlpatterns = [
    # Product URLs
    path('products/', views.products_list, name='products_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('products/export/csv/', views.export_products_csv, name='export_products_csv'),
    path('products/export/pdf/', views.export_products_pdf, name='export_products_pdf'),
    path('products/import/', views.import_products, name='import_products'),
    
    # Supplier URLs
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    
    # Purchase Order URLs
    path('purchase-orders/', views.purchase_orders_list, name='purchase_orders_list'),
    path('purchase-orders/create/', views.purchase_order_create, name='purchase_order_create'),
    path('purchase-orders/update/<int:pk>/', views.purchase_order_update, name='purchase_order_update'),
    path('purchase-orders/delete/<int:pk>/', views.purchase_order_delete, name='purchase_order_delete'),
]
