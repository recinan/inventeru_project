from django import forms
from .models import Warehouse

class WarehouseForm(forms.ModelForm):
    warehouse_name = forms.CharField()
    class Meta:
        model = Warehouse
        fields = ['warehouse_name']
    
