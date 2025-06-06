from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Category
from .forms import CategoryForm, CategoryFormWarehouse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from warehouse_man.models import Warehouse
from inventory_man.models import InventoryItem
import re
from django.core.paginator import Paginator
from util_funcs.Paginator import PaginatorClass

# Create your views here.

@login_required(login_url='login')
def add_category_warehouse(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user,slug = warehouse_slug)
    warehouse_category_count = Category.objects.filter(user=request.user, warehouse=warehouse).count()
    warehouse_category_count_limit = request.user.get_category_per_warehouse_limit()

    if warehouse_category_count >= warehouse_category_count_limit:
        messages.error(request, "You achieved your category limit!")
        return redirect(reverse_lazy('list-category',kwargs={'warehouse_slug':warehouse_slug}))

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

@login_required(login_url='login')
def list_categories(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug = warehouse_slug)
    category_list = Category.objects.filter(user = request.user, warehouse = warehouse,category_name__contains = request.GET.get('searchCategory','')).order_by('-date_created')
    inventory_items = InventoryItem.objects.filter(user=request.user,warehouse=warehouse).order_by('-date_created')
    """
    p = Paginator(category_list,3)
    page = request.GET.get('category_page')
    categories = p.get_page(page)"""
    categories = PaginatorClass.paginator(request,category_list,3,'category_page')

    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':categories,
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
    warehouse = get_object_or_404(Warehouse, user=request.user ,slug = warehouse_slug)

    search_filter = request.GET.get('searchCategory', '').strip()

    if not re.match(r'^[\w\s-]*$', search_filter):
        search_filter = ''

    category_list = Category.objects.filter(user = request.user, warehouse = warehouse,category_name__contains = search_filter).order_by('-date_created')
    inventory_items = InventoryItem.objects.filter(user=request.user,warehouse=warehouse).order_by('-date_created')
    """
    p = Paginator(category_list,3)
    page = request.GET.get('category_page')
    categories = p.get_page(page)
    """
    categories = PaginatorClass.paginator(request,category_list,3,'category_page')
   
    """
    p_item = Paginator(inventory_items,15)
    page_item = request.GET.get('item_page')
    items = p_item.get_page(page_item)"""
    items = PaginatorClass.paginator(request,inventory_items,15,'item_page')

    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':categories,
        'all_items':items
    }
    return render(request, 'category_man/list_category.html', context)

@login_required(login_url='login')
def delete_category(request,warehouse_slug,category_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug=warehouse_slug)
    category = get_object_or_404(Category, warehouse=warehouse,slug = category_slug)
    if request.method == 'POST':
        category.delete()
        return redirect(reverse_lazy('list-item',kwargs={'warehouse_slug':warehouse_slug}))
    context = {
        'category':category
    }
    return render(request,'category_man/delete_category.html',context)
