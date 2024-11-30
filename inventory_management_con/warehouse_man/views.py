from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import WarehouseForm

# Create your views here.

login_required(login_url='login')
def add_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('dashboard'))
    else:
        form = WarehouseForm()

    context = {
        'form':form
    }
    return render(request, 'add_warehouse.html',context)
