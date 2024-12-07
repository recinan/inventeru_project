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
        form = WarehouseForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect(reverse_lazy('list-warehouse'))
    else:
        form = WarehouseForm(user=request.user)

    context = {
        'form':form
    }
    return render(request, 'warehouse_man/add_warehouse.html',context)

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
