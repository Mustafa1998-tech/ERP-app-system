"""
Pytest configuration and fixtures for the ERP project tests.
"""
import os
import pytest
from django.test import Client
from django.contrib.auth.models import User as DjangoUser
from sales.models import Customer, Order, Invoice
from inventory.models import Product, Supplier, PurchaseOrder

# Ensure Django settings are configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')

@pytest.fixture
def client():
    """Return a Django test client."""
    return Client()

@pytest.fixture
def admin_user():
    """Create and return an admin user."""
    return DjangoUser.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(client, admin_user):
    """Return a client logged in as admin."""
    client.login(username='admin', password='testpass123')
    return client

@pytest.fixture
def customer():
    """Create and return a test customer."""
    return Customer.objects.create(
        name='Test Customer',
        email='test@example.com',
        phone='1234567890',
        address='123 Test Street'
    )

@pytest.fixture
def product():
    """Create and return a test product."""
    return Product.objects.create(
        name='Test Product',
        sku='TEST-001',
        price=99.99,
        quantity=100,
        description='Test product description'
    )

@pytest.fixture
def supplier():
    """Create and return a test supplier."""
    return Supplier.objects.create(
        name='Test Supplier',
        email='supplier@example.com',
        phone='0987654321',
        address='456 Supplier Ave'
    )

@pytest.fixture
def order(customer):
    """Create and return a test order."""
    return Order.objects.create(
        customer=customer,
        order_date='2024-01-01',
        total_amount=299.99,
        status='pending'
    )

@pytest.fixture
def invoice(order):
    """Create and return a test invoice."""
    return Invoice.objects.create(
        order=order,
        invoice_date='2024-01-02',
        amount=299.99,
        status='unpaid'
    )

@pytest.fixture
def purchase_order(supplier):
    """Create and return a test purchase order."""
    return PurchaseOrder.objects.create(
        supplier=supplier,
        order_date='2024-01-01',
        total_amount=500.00,
        status='pending'
    )
