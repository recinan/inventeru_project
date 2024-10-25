from django.shortcuts import render,redirect
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
            item = form.save()
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