from django import forms
from .models import Warehouse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
import re


class WarehouseForm(forms.ModelForm):
    warehouse_name = forms.CharField()
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'(XXX) XXX XXXX'}))
    class Meta:
        model = Warehouse
        fields = ['warehouse_name','phone_number','neighborhood','street','district','city','postal_code','country']

    def clean_warehouse_name(self):
        warehouse_name = self.cleaned_data.get('warehouse_name')
        slug = slugify(warehouse_name)
        
        if Warehouse.objects.filter(user=self.user,slug=slug).exclude(pk=self.instance.pk).exists():
            raise ValidationError(f'{warehouse_name} already exists!')
        return warehouse_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number:
            clean_number = re.sub(r'\D','',phone_number)

            if len(clean_number) != 10:
                raise ValidationError('Phone number must be 10 or 11 digits long!')
            
            formatted_number = f"({clean_number[:3]}) {clean_number[3:6]} {clean_number[6:10]}"
            return formatted_number
        
        return phone_number

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
    

    

