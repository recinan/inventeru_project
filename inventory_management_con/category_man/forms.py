from django import forms
from django.contrib.auth.models import User
from warehouse_man.models import Warehouse
from .models import Category


class CategoryForm(forms.ModelForm):
    category_name = forms.CharField()
    #warehouse = forms.CharField()
    class Meta:
        model = Category
        fields = ['category_name','warehouse']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)
        if self.user:
            self.fields['warehouse'].queryset = Warehouse.objects.filter(user=self.user.id)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    
class CategoryFormWarehouse(forms.ModelForm):
    category_name = forms.CharField()
    #warehouse = forms.CharField()
    class Meta:
        model = Category
        fields = ['category_name']

    def __init__(self, *args, user=None, warehouse=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.warehouse = warehouse

        if warehouse:
                self.fields['category_name'].queryset = Category.objects.filter(warehouse=warehouse)
