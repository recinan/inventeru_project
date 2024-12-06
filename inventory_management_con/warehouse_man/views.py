from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import WarehouseForm
from .models import Warehouse

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
