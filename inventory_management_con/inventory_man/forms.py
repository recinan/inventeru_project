from django import forms
from django.contrib.auth.models import User
from inventory_man.models import InventoryItem
from warehouse_man.models import Warehouse
from category_man.models import Category

class InventoryItemForm(forms.ModelForm):
    #category = forms.ModelChoiceField(queryset=Category.objects.filter(), initial=0)
    #warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), initial=0)
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'quantity','category','warehouse']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
        if user:
            #self.fields['category'].queryset = Category.objects.filter(user=user.id)
            self.fields['warehouse'].queryset = Warehouse.objects.filter(user=user.id)

            warehouse_id = kwargs.get('initial',{}).get('warehouse',None)
            if warehouse_id:
                self.fields['category'].queryset = Category.objects.filter(user=user,warehouse__id = warehouse_id)
            else:
                self.fields['category'].queryset = Category.objects.filter(user=user)

    def save(self, commit = False):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

"""
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
        return instance"""