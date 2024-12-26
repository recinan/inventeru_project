from django import forms
from .models import Warehouse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class WarehouseForm(forms.ModelForm):
    warehouse_name = forms.CharField()
    class Meta:
        model = Warehouse
        fields = ['warehouse_name','phone_number','neighborhood','street','district','city','postal_code','country']

    def clean_warehouse_name(self):
        warehouse_name = self.cleaned_data.get('warehouse_name')
        slug = slugify(warehouse_name)
        
        if Warehouse.objects.filter(user=self.user,slug=slug).exclude(pk=self.instance.pk).exists():
            raise ValidationError(f'{warehouse_name} already exists!')
        return warehouse_name
   

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    

