from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import InventoryItem,Category
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm, CategoryForm
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    items = InventoryItem.objects.filter(user=request.user.id).order_by('id')
    
    low_inventory = InventoryItem.objects.filter(
        user = request.user.id,
        quantity__lte = LOW_QUANTITY
    )

    low_inventory_count = low_inventory.count()
    if low_inventory_count > 0:
        if low_inventory_count > 1:
            messages.error(request, f'{low_inventory_count} items have low inventory')
        else:
            messages.error(request, f'{low_inventory_count} item has low inventory')

    low_inventory_ids = low_inventory.values_list('id',flat=True)

    return render(request, 'dashboard.html',{
        'items':items,
        'low_inventory_ids':low_inventory_ids
    })

@login_required(login_url='login')
def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            print(request.user)
            return redirect(reverse_lazy('dashboard'))
    else:
        form = InventoryItemForm()

    categories = Category.objects.all()
    context = {
        'form':form,
        'categories':categories
    }
    return render(request, 'item_form.html',context)

@login_required(login_url='login')
def edit_item(request, pk):
    item = get_object_or_404(InventoryItem, pk = pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('dashboard'))
    else:
        form = InventoryItemForm(instance=item)

    context = {
        'form':form
    }

    return render(request, 'item_form.html',context)

@login_required(login_url='login')
def delete_item(request, pk):
    item = get_object_or_404(InventoryItem, pk = pk)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse_lazy('dashboard'))
    return render(request, 'delete_item.html')


@login_required(login_url="login")
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('dashboard'))
    else:
        form = CategoryForm()

    context = {
        'form' :form
    }
    return render(request,'add_category.html',context)

