from django.test import TestCase
from .models import CustomUser
from accounts.forms import UserRegisterForm
from django_recaptcha.fields import ReCaptchaField
from .forms import UserLoginForm 
from django import forms
from unittest.mock import patch

class UserRegisterFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'phone_number': '(123) 456 7890',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }

    def test_form_valid_data(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        data = self.valid_data.copy()
        data.pop('email')  
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_phone_number_formatting(self):
        data = self.valid_data.copy()
        data['phone_number'] = '1234567890' 
        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        self.assertEqual(user.phone_number, '(123) 456 7890')  

    def test_invalid_phone_number_length(self):
        data = self.valid_data.copy()
        data['phone_number'] = '12345'  
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'][0], 'Phone number must be 10 or 11 digits long!')

    def test_form_password_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPassword123!'  
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_save_method(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, CustomUser)  
        self.assertEqual(user.email, 'johndoe@example.com')  

    def test_help_texts(self):
        form = UserRegisterForm()
        self.assertEqual(form.fields['email'].help_text, "A valid email address for verification, please.")
        self.assertEqual(form.fields['username'].help_text, "Choose a unique username, please.")
        self.assertEqual(form.fields['phone_number'].help_text, "Choose a unique phone number, please.")

