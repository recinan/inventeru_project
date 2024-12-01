from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required(login_url="login")
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user = request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('dashboard'))
    else:
        form = CategoryForm(user = request.user)

    context = {
        'form' :form
    }
    return render(request,'add_category.html',context)

@login_required
def get_categories_for_warehouse(request, warehouse_id):
    categories = Category.objects.filter(warehouse_id=warehouse_id)
    category_list = [{"id": category.id, "name": category.category_name} for category in categories]
    return JsonResponse({"categories": category_list})