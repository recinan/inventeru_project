from django.test import TestCase
from .models import InventoryItem
from category_man.models import Category
from warehouse_man.models import Warehouse
from accounts.models import CustomUser
from .forms import InventoryItemFormWarehouse
from django.contrib.auth.models import User

class InventoryItemFormWarehouseTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")

        self.warehouse = Warehouse.objects.create(
            warehouse_name="Test Warehouse",
            user=self.user,
            district="Test District",
            postal_code="12345",
            city="Test City",
            country="Test Country"
        )

        self.category = Category.objects.create(
            category_name="Test Category",
            warehouse=self.warehouse,
            user=self.user
        )

        self.inventory_item = InventoryItem.objects.create(
            user=self.user,
            warehouse=self.warehouse,
            category = self.category,
            item_name="Test Item",
            quantity=10,
            unit="pcs",
            price=100,
            currency="USD",
            description="Test Description",
        )

    def test_valid_form(self):
        form_data = {
            'item_name': 'New Item',
            'quantity': 5,
            'unit': 'pcs',
            'price': 50,
            'currency': 'USD',
            'description': 'A new test item.',
        }
        form = InventoryItemFormWarehouse(data=form_data, user=self.user, warehouse=self.warehouse)
        self.assertTrue(form.is_valid())

    def test_duplicate_item_name(self):
        form_data = {
            'item_name': 'Test Item',  
            'quantity': 5,
            'unit': 'pcs',
            'price': 50,
            'currency': 'USD',
            'description': 'A duplicate test item.',
        }
        form = InventoryItemFormWarehouse(data=form_data, user=self.user, warehouse=self.warehouse)
        self.assertFalse(form.is_valid())
        self.assertIn('item_name', form.errors)
        self.assertEqual(form.errors['item_name'][0], 'Test Item already exists in this warehouse!')

    def test_negative_price(self):
        form_data = {
            'item_name': 'Negative Price Item',
            'quantity': 5,
            'unit': 'pcs',
            'price': -10,  
            'currency': 'USD',
            'description': 'Test item with negative price.',
        }
        form = InventoryItemFormWarehouse(data=form_data, user=self.user, warehouse=self.warehouse)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertEqual(form.errors['price'][0], 'Price cannot be less than zero !')

    def test_negative_quantity(self):
        form_data = {
            'item_name': 'Negative Quantity Item',
            'quantity': -5,  
            'unit': 'pcs',
            'price': 50,
            'currency': 'USD',
            'description': 'Test item with negative quantity.',
        }
        form = InventoryItemFormWarehouse(data=form_data, user=self.user, warehouse=self.warehouse)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)
        self.assertEqual(form.errors['quantity'][0], 'Quantity cannot be less than zero !')

    def test_missing_user_or_warehouse(self):
        form_data = {
            'item_name': 'No User/Warehouse Item',
            'quantity': 5,
            'unit': 'pcs',
            'price': 50,
            'currency': 'USD',
            'description': 'Test item without user or warehouse.',
        }
        form = InventoryItemFormWarehouse(data=form_data)  
        self.assertFalse(form.is_valid())
        self.assertIn('item_name', form.errors)
        self.assertEqual(form.errors['item_name'][0], 'User or warehouse information is missing.')
