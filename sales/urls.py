from django.urls import path
from . import views

app_name = 'sales'  # Add this line for namespace support

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Customer URLs
    path('customers/', views.customers_list, name='customers_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/update/<int:pk>/', views.customer_update, name='customer_update'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    path('customers/export/<str:format_type>/', views.export_customers, name='export_customers'),
    path('customers/import/', views.import_customers, name='import_customers'),
    
    # Order URLs
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/update/<int:pk>/', views.order_update, name='order_update'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orders/export/<str:format_type>/', views.export_orders, name='export_orders'),
    path('orders/import/', views.import_orders, name='import_orders'),
    
    # Invoice URLs
    path('invoices/', views.invoices_list, name='invoices_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/update/<int:pk>/', views.invoice_update, name='invoice_update'),
    path('invoices/delete/<int:pk>/', views.invoice_delete, name='invoice_delete'),
    path('invoices/export/<str:format_type>/', views.export_invoices, name='export_invoices'),
    path('invoices/import/', views.import_invoices, name='import_invoices'),
]
