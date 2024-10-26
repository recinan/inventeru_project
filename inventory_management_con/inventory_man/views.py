from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import InventoryItem,Category
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    items = InventoryItem.objects.filter(user=request.user.id).order_by('id')
    return render(request, 'dashboard.html',{
        'items':items
    })

@login_required
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

@login_required
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