from django import forms
from inventory_man.models import Category, InventoryItem
from warehouse_man.models import Warehouse

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all())
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity','category','warehouse']

class CategoryForm(forms.ModelForm):
    category = forms.CharField()
    class Meta:
        model = Category
        fields = ['category']
