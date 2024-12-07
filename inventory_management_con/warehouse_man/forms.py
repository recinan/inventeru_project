from django import forms
from .models import Warehouse


class WarehouseForm(forms.ModelForm):
    warehouse_name = forms.CharField()
    class Meta:
        model = Warehouse
        fields = ['warehouse_name','address','phone_number']

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
