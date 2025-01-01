# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from warehouse_man.models import Warehouse
from warehouse_man.forms import WarehouseForm

User = get_user_model()

class WarehouseFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.warehouse_data = {
            'warehouse_name': 'Test Warehouse',
            'phone_number': '1234567890',
            'neighborhood': 'Test Neighborhood',
            'street': 'Test Street',
            'district': 'Test District',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Türkiye',
        }

    def test_valid_form(self):
        form = WarehouseForm(data=self.warehouse_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_missing_user(self):
        form = WarehouseForm(data=self.warehouse_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_warehouse_name(self):
        Warehouse.objects.create(
            warehouse_name='Test Warehouse',
            user=self.user,
            district='Test District',
            city='Test City',
            postal_code='12345',
            country='Türkiye'
        )
        form = WarehouseForm(data=self.warehouse_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('warehouse_name', form.errors)
        self.assertEqual(form.errors['warehouse_name'][0], 'Test Warehouse already exists!')

    def test_invalid_phone_number(self):
        invalid_data = self.warehouse_data.copy()
        invalid_data['phone_number'] = '123'
        form = WarehouseForm(data=invalid_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'][0], 'Phone number must be 10 or 11 digits long!')

    def test_clean_phone_number(self):
        valid_data = self.warehouse_data.copy()
        valid_data['phone_number'] = '(123) 456-7890'
        form = WarehouseForm(data=valid_data, user=self.user)
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertEqual(instance.phone_number, '(123) 456 7890')

    def test_save_form(self):
        form = WarehouseForm(data=self.warehouse_data, user=self.user)
        self.assertTrue(form.is_valid())
        warehouse = form.save()
        self.assertEqual(warehouse.user, self.user)
        self.assertEqual(warehouse.warehouse_name, 'Test Warehouse')
