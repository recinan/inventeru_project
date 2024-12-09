from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import InventoryItem
from category_man.models import Category
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm, InventoryItemFormWarehouse
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import JsonResponse
from warehouse_man.models import Warehouse

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

    return render(request, 'inventory_man/dashboard.html',{
        'items':items,
        'low_inventory_ids':low_inventory_ids
    })

def list_item(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    category_list = Category.objects.filter(user = request.user, warehouse=warehouse)
    inventory_items = InventoryItem.objects.filter(user=request.user,warehouse=warehouse)
    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':category_list,
        'all_items':inventory_items
    }
    return render(request,'category_man/list_category.html',context)

def list_item_category(request, warehouse_slug, category_slug):
    warehouse = get_object_or_404(Warehouse, slug=warehouse_slug)
    all_categories = Category.objects.filter(user = request.user,warehouse=warehouse)
    category = get_object_or_404(Category, slug = category_slug)
    inventory_items = InventoryItem.objects.filter(user=request.user,category=category)
    context = {
        'warehouse_slug':warehouse_slug,
        'categorylist':all_categories,
        'all_items':inventory_items
    }
    return render(request,'category_man/list_category.html',context)

@login_required(login_url='login')
def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, user=request.user)
        if form.is_valid():
            print("Form geçerli", form.cleaned_data)
            #form.save(commit=False)
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            print(request.user)
            return redirect(reverse_lazy('dashboard'))
    else:
        form = InventoryItemForm(user=request.user)

    categories = Category.objects.all()
    context = {
        'form':form,
        'categories':categories
    }
    return render(request, 'inventory_man/item_form.html',context)

@login_required(login_url='login')
def add_item_warehouse(request, warehouse_slug ,category_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    category = get_object_or_404(Category, slug = category_slug, warehouse=warehouse)
    if request.method == 'POST':
        form = InventoryItemFormWarehouse(request.POST, user=request.user, warehouse = warehouse, category = category)
        if form.is_valid():
            print("Form geçerli", form.cleaned_data)
            #form.save(commit=False)
            item = form.save(commit=False)
            item.user = request.user
            item.warehouse = warehouse
            item.category = category
            item.save()
            print(request.user)
            return redirect(reverse_lazy('list-item-category',kwargs={'warehouse_slug':warehouse_slug, 'category_slug':category_slug}))
    else:
        form = InventoryItemFormWarehouse(user=request.user,warehouse=warehouse,category=category)

    categories = Category.objects.all()
    context = {
        'form':form,
        'warehouse':warehouse,
        'category':category,
    }
    return render(request, 'inventory_man/item_form_warehouse.html',context)

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

    return render(request, 'inventory_man/item_form.html',context)

def item_detail(request, warehouse_slug, category_slug, item_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    category = get_object_or_404(Category, slug=category_slug)
    item = get_object_or_404(InventoryItem, warehouse=warehouse, category=category, slug=item_slug)
    if request.method == 'POST':
        form = InventoryItemFormWarehouse(request.POST, instance = item)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('list-item',kwargs={'category_slug':category_slug}))
    else:
        form = InventoryItemFormWarehouse(instance = item)
    
    context = {
        'form':form
    }

    return render(request, 'inventory_man/item_form_warehouse.html',context)

def search_product_bar(request,warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug=warehouse_slug)
    category_list = Category.objects.filter(user=request.user, warehouse=warehouse)
    inventory_items = InventoryItem.objects.filter(user=request.user, warehouse=warehouse, item_name__contains = request.GET['searchProduct'])
    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':category_list,
        'all_items':inventory_items
    }
    return render(request, 'category_man/list_category.html',context)

@login_required(login_url='login')
def delete_item(request, pk):
    item = get_object_or_404(InventoryItem, pk = pk)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse_lazy('dashboard'))
    context = {
        'item':item
    }
    return render(request, 'inventory_man/delete_item.html', context)


