# Create your tests here.

from django.test import TestCase
from warehouse_man.models import Warehouse
from .models import Category
from .forms import CategoryFormWarehouse
from accounts.models import CustomUser

class CategoryFormWarehouseTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(username="testuser", password="password")

        # Create a warehouse
        self.warehouse = Warehouse.objects.create(
            warehouse_name="Test Warehouse",
            user=self.user,
            district="Test District",
            postal_code="12345",
            city="Test City",
            country="Test Country"
        )

        # Create a category
        self.category = Category.objects.create(
            category_name="Test Category",
            warehouse=self.warehouse,
            user=self.user
        )

    def test_valid_form(self):
        form_data = {
            'category_name': 'New Category',
        }
        form = CategoryFormWarehouse(data=form_data, user=self.user, warehouse=self.warehouse)
        self.assertTrue(form.is_valid())

    def test_duplicate_category_name(self):
        form_data = {
            'category_name': 'Test Category',  # Duplicate name
        }
        form = CategoryFormWarehouse(data=form_data, user=self.user, warehouse=self.warehouse)
        self.assertFalse(form.is_valid())
        self.assertIn('category_name', form.errors)
        self.assertEqual(form.errors['category_name'][0], 'Test Category category already exists!')
    
    def test_missing_user_or_warehouse(self):
        form_data = {
            'category_name': 'New Category',
        }
        form = CategoryFormWarehouse(data=form_data)  # No user or warehouse provided
        self.assertFalse(form.is_valid())

    def test_queryset_filter_by_warehouse(self):
        # Create a new warehouse and category
        another_warehouse = Warehouse.objects.create(
            warehouse_name="Another Warehouse",
            user=self.user,
            district="Another District",
            postal_code="54321",
            city="Another City",
            country="Another Country"
        )

        another_category = Category.objects.create(
            category_name="Another Category",
            warehouse=another_warehouse,
            user=self.user
        )

        form = CategoryFormWarehouse(user=self.user, warehouse=self.warehouse)
        self.assertNotIn(another_category, form.fields['category_name'].queryset)
        self.assertIn(self.category, form.fields['category_name'].queryset)

