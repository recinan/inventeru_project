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
        #warehouse = kwargs.pop('warehouse',None)
        super().__init__(*args, **kwargs)
        if user:
            #self.fields['category'].queryset = Category.objects.filter(user=user.id)
            self.fields['warehouse'].queryset = Warehouse.objects.filter(user=user.id)
            #self.fields['category'].queryset = Category.objects.filter(user=user.id, warehouse=warehouse)

            warehouse= kwargs.get('warehouse',None)
            if warehouse:
                self.fields['category'].queryset = Category.objects.filter(user=user,warehouse = warehouse)
            else:
                self.fields['category'].queryset = Category.objects.filter(user=user)

    def save(self, commit = False):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
class InventoryItemFormWarehouse(forms.ModelForm):
    #category = forms.ModelChoiceField(queryset=Category.objects.filter(), initial=0)
    #warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), initial=0)
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'quantity']
    
    def __init__(self, *args,user=None,warehouse=None,category=None, **kwargs):
        user = kwargs.pop('user',None)
        #warehouse = kwargs.pop('warehouse',None)
        super().__init__(*args, **kwargs)
        self.user = user
        self.warehouse = warehouse
        self.category = category

       

