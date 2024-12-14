from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm, CategoryFormWarehouse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from warehouse_man.models import Warehouse
from inventory_man.models import InventoryItem
import re

# Create your views here.

@login_required(login_url="login")
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user = request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('list-allcategories'))
    else:
        form = CategoryForm(user = request.user)

    context = {
        'form' :form
    }
    return render(request,'category_man/add_category.html',context)

@login_required(login_url='login')
def add_category_warehouse(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    if request.method == 'POST':
        form = CategoryFormWarehouse(request.POST, user = request.user, warehouse = warehouse)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.warehouse = warehouse
            item.save()
            return redirect(reverse_lazy('list-category',kwargs={'warehouse_slug': warehouse_slug}))
    else:
        form = CategoryFormWarehouse(user = request.user,warehouse=warehouse)

    context = {
        'warehouse':warehouse,
        'form' :form
    }
    return render(request,'category_man/add_category.html',context)

@login_required
def get_categories_for_warehouse(request, warehouse_id):
    categories = Category.objects.filter(warehouse_id=warehouse_id)
    category_list = [{"id": category.id, "name": category.category_name} for category in categories]
    return JsonResponse({"categories": category_list})

@login_required(login_url='login')
def list_categories(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    category_list = Category.objects.filter(user = request.user, warehouse = warehouse,category_name__contains = request.GET.get('searchCategory',''))
    inventory_items = InventoryItem.objects.filter(user=request.user,warehouse=warehouse)
    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':category_list,
        'all_items':inventory_items
    }
    return render(request, 'category_man/list_category.html', context)

@login_required(login_url='login')
def list_allcategories(request):
    all_categories = Category.objects.filter(user=request.user)
    context = {
        'categorylist':all_categories
    }
    return render(request, 'category_man/list_category.html',context)

@login_required(login_url='login')
def search_category_bar(request,warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)

    search_filter = request.GET.get('searchCategory', '').strip()

    if not re.match(r'^[\w\s-]*$', search_filter):
        search_filter = ''

    category_list = Category.objects.filter(user = request.user, warehouse = warehouse,category_name__contains = search_filter)
    inventory_items = InventoryItem.objects.filter(user=request.user,warehouse=warehouse)
    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':category_list,
        'all_items':inventory_items
    }
    return render(request, 'category_man/list_category.html', context)

@login_required(login_url='login')
def delete_category(request,category_slug):
    item = get_object_or_404(Category, slug = category_slug)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse_lazy('dashboard'))
    context = {
        'category':item
    }
    return render(request,'category_man/delete_category.html',context)
