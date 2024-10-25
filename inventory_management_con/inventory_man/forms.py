from django import forms
from inventory_man.models import Category, InventoryItem

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity','category']