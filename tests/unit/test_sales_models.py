"""
Unit tests for sales models.
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from sales.models import Customer, Order, Invoice

@pytest.mark.django_db
class TestCustomerModel:
    """Test cases for Customer model."""
    
    def test_customer_creation(self):
        """Test creating a customer."""
        customer = Customer.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Main St'
        )
        assert customer.name == 'John Doe'
        assert customer.email == 'john@example.com'
        assert str(customer) == 'John Doe'
    
    def test_customer_str_method(self):
        """Test customer string representation."""
        customer = Customer(name='Jane Smith')
        assert str(customer) == 'Jane Smith'

@pytest.mark.django_db
class TestOrderModel:
    """Test cases for Order model."""
    
    def test_order_creation(self, customer):
        """Test creating an order."""
        order = Order.objects.create(
            customer=customer,
            order_date='2024-01-01',
            total_amount=Decimal('299.99'),
            status='pending'
        )
        assert order.customer == customer
        assert order.total_amount == Decimal('299.99')
        assert order.status == 'pending'
        assert str(order) == f"Order #{order.id} - {customer.name}"
    
    def test_order_default_status(self, customer):
        """Test order default status."""
        order = Order.objects.create(
            customer=customer,
            order_date='2024-01-01',
            total_amount=Decimal('100.00')
        )
        assert order.status == 'pending'

@pytest.mark.django_db
class TestInvoiceModel:
    """Test cases for Invoice model."""
    
    def test_invoice_creation(self, order):
        """Test creating an invoice."""
        invoice = Invoice.objects.create(
            order=order,
            invoice_date='2024-01-02',
            amount=Decimal('299.99'),
            status='unpaid'
        )
        assert invoice.order == order
        assert invoice.amount == Decimal('299.99')
        assert invoice.status == 'unpaid'
        assert str(invoice) == f"Invoice #{invoice.id} - {order.customer.name}"
    
    def test_invoice_default_status(self, order):
        """Test invoice default status."""
        invoice = Invoice.objects.create(
            order=order,
            invoice_date='2024-01-02',
            amount=Decimal('299.99')
        )
        assert invoice.status == 'unpaid'
