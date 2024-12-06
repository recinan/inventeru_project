from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm, CategoryFormWarehouse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from warehouse_man.models import Warehouse

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
        'form' :form
    }
    return render(request,'category_man/add_category.html',context)

@login_required
def get_categories_for_warehouse(request, warehouse_id):
    categories = Category.objects.filter(warehouse_id=warehouse_id)
    category_list = [{"id": category.id, "name": category.category_name} for category in categories]
    return JsonResponse({"categories": category_list})

def list_categories(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    category_list = Category.objects.filter(user = request.user, warehouse = warehouse)
    context = {
        'categorylist':category_list
    }
    return render(request, 'category_man/list_category.html', context)

def list_allcategories(request):
    all_categories = Category.objects.filter(user=request.user)
    context = {
        'categorylist':all_categories
    }
    return render(request, 'category_man/list_category.html',context)