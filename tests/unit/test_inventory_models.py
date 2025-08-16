"""
Unit tests for inventory models.
"""
import pytest
from decimal import Decimal
from inventory.models import Product, Supplier, PurchaseOrder

@pytest.mark.django_db
class TestProductModel:
    """Test cases for Product model."""
    
    def test_product_creation(self):
        """Test creating a product."""
        product = Product.objects.create(
            name='Test Laptop',
            sku='LAP-001',
            price=Decimal('999.99'),
            quantity=50,
            description='High-performance laptop'
        )
        assert product.name == 'Test Laptop'
        assert product.sku == 'LAP-001'
        assert product.price == Decimal('999.99')
        assert product.quantity == 50
        assert str(product) == 'Test Laptop'
    
    def test_product_sku_unique(self):
        """Test product SKU uniqueness."""
        Product.objects.create(
            name='Product 1',
            sku='UNIQUE-001',
            price=Decimal('100.00'),
            quantity=10
        )
        with pytest.raises(Exception):
            Product.objects.create(
                name='Product 2',
                sku='UNIQUE-001',
                price=Decimal('200.00'),
                quantity=20
            )

@pytest.mark.django_db
class TestSupplierModel:
    """Test cases for Supplier model."""
    
    def test_supplier_creation(self):
        """Test creating a supplier."""
        supplier = Supplier.objects.create(
            name='Tech Supplies Inc',
            email='contact@techsupplies.com',
            phone='555-1234',
            address='123 Business Ave'
        )
        assert supplier.name == 'Tech Supplies Inc'
        assert supplier.email == 'contact@techsupplies.com'
        assert str(supplier) == 'Tech Supplies Inc'

@pytest.mark.django_db
class TestPurchaseOrderModel:
    """Test cases for PurchaseOrder model."""
    
    def test_purchase_order_creation(self, supplier):
        """Test creating a purchase order."""
        po = PurchaseOrder.objects.create(
            supplier=supplier,
            order_date='2024-01-01',
            total_amount=Decimal('5000.00'),
            status='pending'
        )
        assert po.supplier == supplier
        assert po.total_amount == Decimal('5000.00')
        assert po.status == 'pending'
        assert str(po) == f"PO #{po.id} - {supplier.name}"
    
    def test_purchase_order_default_status(self, supplier):
        """Test purchase order default status."""
        po = PurchaseOrder.objects.create(
            supplier=supplier,
            order_date='2024-01-01',
            total_amount=Decimal('1000.00')
        )
        assert po.status == 'pending'
