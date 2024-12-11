from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import WarehouseForm
from .models import Warehouse
from inventory_man.models import InventoryItem
from category_man.models import Category

# Create your views here.

@login_required(login_url='login')
def list_warehouse(request):
    warehouse_list = Warehouse.objects.filter(user = request.user.id)
    context = {
        'warehouselist':warehouse_list
    }
    return render(request, 'warehouse_man/list_warehouse.html',context)

login_required(login_url='login')
def add_warehouse(request):
    if request.method == 'POST':
        warehouse_form= WarehouseForm(request.POST, user=request.user)
        if warehouse_form.is_valid():
            warehouse = warehouse_form.save(commit=False)
            warehouse.user = request.user
            warehouse.save()
            return redirect(reverse_lazy('list-warehouse'))
    else:
        warehouse_form= WarehouseForm(user=request.user)

    context = {
        'warehouse_form':warehouse_form
    }
    return render(request, 'warehouse_man/add_warehouse.html',context)

@login_required(login_url='login')
def warehouse_detail(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user = request.user,slug = warehouse_slug)
    categories = Category.objects.filter(user = request.user, warehouse=warehouse)
    items = InventoryItem.objects.filter(user = request.user, warehouse=warehouse)
    context = {
        'warehouse':warehouse,
        'categories':categories,
        'items':items
    }
    
    return render(request, 'warehouse_man/warehouse-detail.html',context)
