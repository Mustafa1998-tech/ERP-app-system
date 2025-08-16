"""
Integration tests for sales views.
"""
import pytest
from django.urls import reverse
from sales.models import Customer, Order
from inventory.models import Product

@pytest.mark.django_db
class TestSalesViews:
    """Test cases for sales views."""
    
    def test_dashboard_view(self, client, customer):
        """Test the dashboard view."""
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200
        assert 'customers_count' in response.context
        assert 'orders_count' in response.context
        assert 'invoices_count' in response.context

    def test_customers_list_view(self, client, customer):
        """Test the customers list view."""
        response = client.get(reverse('customers_list'))
        assert response.status_code == 200
        assert customer in response.context['customers']

    def test_customer_create_view(self, client):
        """Test the customer create view."""
        response = client.post(reverse('customer_create'), {
            'name': 'New Customer',
            'email': 'newcustomer@example.com',
            'phone': '1234567890',
            'address': '789 New St'
        })
        assert response.status_code == 302  # Redirect after successful creation
        assert Customer.objects.filter(name='New Customer').exists()

    def test_order_create_view(self, client, customer):
        """Test the order create view."""
        product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            price=100.00,
            quantity=10
        )
        response = client.post(reverse('order_create'), {
            'customer': customer.id,
            'order_date': '2024-01-01',
            'total_amount': 100.00,
            'status': 'pending'
        })
        assert response.status_code == 302  # Redirect after successful creation
        assert Order.objects.filter(customer=customer).exists()
