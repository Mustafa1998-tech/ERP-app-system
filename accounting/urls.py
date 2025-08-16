from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Ledger URLs
    path('ledgers/', views.ledgers_list, name='ledgers_list'),
    path('ledgers/create/', views.ledger_create, name='ledger_create'),
    path('ledgers/export/<str:format_type>/', views.export_ledgers, name='export_ledgers'),
    path('ledgers/import/', views.import_ledgers, name='import_ledgers'),
    path('ledgers/<int:pk>/edit/', views.ledger_update, name='ledger_update'),
    path('ledgers/<int:pk>/delete/', views.ledger_delete, name='ledger_delete'),
    
    # Transaction URLs
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/export/<str:format_type>/', views.export_transactions, name='export_transactions'),
    path('transactions/import/', views.import_transactions, name='import_transactions'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # Report URLs
    path('reports/', views.reports_list, name='reports_list'),
    path('reports/generate/<str:report_type>/', views.report_generate, name='report_generate'),
    path('reports/export/<str:format_type>/', views.export_reports, name='export_reports'),
    path('reports/import/', views.import_reports, name='import_reports'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/edit/', views.report_update, name='report_update'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
    
    # Test URL
    path('test/', views.test_template, name='test_template'),
]
