from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import InventoryItem
from category_man.models import Category
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm, InventoryItemFormWarehouse
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from warehouse_man.models import Warehouse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import re
from django.core.paginator import Paginator
from util_funcs.Paginator import PaginatorClass
from django.db.models.functions import Lower

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def dashboard(request):
    items = InventoryItem.objects.filter(user=request.user.id).order_by('id')
    
    return render(request, 'inventory_man/dashboard.html',{
        'items':items
    })

@login_required(login_url='login')
def list_item(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug = warehouse_slug)
    category_list = Category.objects.filter(user = request.user, warehouse=warehouse).order_by('-date_created')
    inventory_items = InventoryItem.objects.filter(user=request.user,warehouse=warehouse).order_by('-date_created')
   
    items = PaginatorClass.paginator(request,inventory_items,15,'item_page')
    categories = PaginatorClass.paginator(request,category_list,3,'category_page')

    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':categories,
        'all_items':items
    }
    return render(request,'category_man/list_category.html',context)

@login_required(login_url='login')
def list_item_category(request, warehouse_slug, category_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug=warehouse_slug)
    all_categories = Category.objects.filter(user = request.user,warehouse=warehouse).order_by('-date_created')
    category = get_object_or_404(Category, user=request.user, warehouse=warehouse,slug = category_slug)
    inventory_items = InventoryItem.objects.filter(user=request.user,category=category).order_by('-date_created')
    """
    p_item = Paginator(inventory_items,15)
    page_item = request.GET.get('item_page')
    items = p_item.get_page(page_item)"""
    items = PaginatorClass.paginator(request,inventory_items,15,'item_page')
    
    """
    p_category = Paginator(all_categories,4)
    page_category = request.GET.get('category_page')
    categories = p_category.get_page(page_category)"""
    categories = PaginatorClass.paginator(request,all_categories,3,'category_page')


    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':categories,
        'all_items':items
    }
    return render(request,'category_man/list_category.html',context)

def list_item_less_than_five(request,warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug=warehouse_slug)
    all_categories = Category.objects.filter(user = request.user,warehouse=warehouse).order_by('date_created').order_by('-date_created')
    #category = get_object_or_404(Category, slug = category_slug)
    inventory_items_less_than_five= InventoryItem.objects.filter(user=request.user,warehouse=warehouse, quantity__lte = 5 ).order_by('-date_created')
    """
    p_item = Paginator(inventory_items_less_than_five,15)
    page_item = request.GET.get('item_page')
    items = p_item.get_page(page_item)"""
    items = PaginatorClass.paginator(request,inventory_items_less_than_five,15,'item_page')

    """
    p_category = Paginator(all_categories,4)
    page_category = request.GET.get('category_page')
    categories = p_category.get_page(page_category)"""
    categories = PaginatorClass.paginator(request,all_categories,3,'category_page')

    context = {
        'warehouse':warehouse,
        'warehouse_slug':warehouse_slug,
        'categorylist':categories,
        'all_items':items
    }

    return render(request, 'category_man/list_category.html',context)

@login_required(login_url='login')
def add_item_warehouse(request, warehouse_slug ,category_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug = warehouse_slug)
    category = get_object_or_404(Category, user=request.user, slug = category_slug, warehouse=warehouse)
    category_product_count = InventoryItem.objects.filter(user=request.user, warehouse=warehouse,category=category).count()
    category_product_count_limit = request.user.get_products_per_category_limit()

    if category_product_count >= category_product_count_limit:
        messages.error(request,"You achieved your product count by category limit!")
        return redirect(reverse_lazy('list-item-category',kwargs={'warehouse_slug':warehouse_slug, 'category_slug':category_slug}))

    if request.method == 'POST':
        form = InventoryItemFormWarehouse(request.POST, request.FILES ,user=request.user, warehouse = warehouse, category = category)
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
def item_detail(request, warehouse_slug, category_slug, item_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user,slug = warehouse_slug)
    category = get_object_or_404(Category, user=request.user,warehouse=warehouse,slug=category_slug)
    item = get_object_or_404(InventoryItem, user=request.user, warehouse=warehouse, category=category, slug=item_slug)
    if request.method == 'POST':
        form = InventoryItemFormWarehouse(request.POST, request.FILES,instance = item, user=request.user, warehouse=warehouse)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('list-item-category',kwargs={'warehouse_slug':warehouse_slug,'category_slug':category_slug}))
    else:
        form = InventoryItemFormWarehouse(instance = item, user=request.user, warehouse=warehouse)
    
    context = {
        'warehouse_slug':warehouse_slug,
        'category_slug':category_slug,
        'item_slug':item_slug,
        'item':item,
        'form':form
    }

    return render(request, 'inventory_man/item_detail.html',context)

@login_required(login_url='login')
def search_product_bar(request,warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug=warehouse_slug)

    search_filter = request.GET.get('searchProduct', '').strip()

    if not re.match(r'^[\w\s-]*$', search_filter):
        search_filter = ''

    category_list = Category.objects.filter(user=request.user, warehouse=warehouse).order_by('-date_created')
    inventory_items = InventoryItem.objects.filter(user=request.user, warehouse=warehouse, item_name__icontains = search_filter).order_by('-date_created')
    """
    p = Paginator(category_list,3)
    page = request.GET.get('category_page')
    categories = p.get_page(page)"""
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
    return render(request, 'category_man/list_category.html',context)

@login_required(login_url='login')
def delete_item(request,pk,warehouse_slug):
    item = get_object_or_404(InventoryItem, pk = pk)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse_lazy('list-item',kwargs={'warehouse_slug':warehouse_slug}))
    context = {
        'item':item
    }
    return render(request, 'inventory_man/delete_item.html', context)

@login_required(login_url='login')
def item_detail_pdf(request,warehouse_slug,category_slug,item_slug):
    warehouse = get_object_or_404(Warehouse,user=request.user, slug=warehouse_slug)
    category = get_object_or_404(Category, user=request.user,slug=category_slug)
    item = get_object_or_404(InventoryItem, slug = item_slug, warehouse=warehouse,category=category)

    # Create ByteStream Buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Page size (width, height)
    page_width, page_height = letter

    c.setFont("Helvetica-Bold",20)
    c.drawString(200,60,"Inventory Manager")
    c.setLineWidth(5)
    c.line(50,100,page_width-50,100)

    #Create a text object
    textob = c.beginText()
    textob.setTextOrigin(80,5*inch)
    textob.setFont("Helvetica",14)
    
    lines = [
        f"Item Name: {item.item_name}",
        f"Quantity: {item.quantity} {item.unit}",
        f"Price: {item.price} {item.currency}",
        f"Description: {item.description}",
        f"Category: {item.category}",
        f"Warehouse: {item.warehouse}",
        f"Adress: {item.warehouse.neighborhood} {item.warehouse.street}",
        f"        {item.warehouse.district} / {item.warehouse.city} {item.warehouse.postal_code}"
    ]

    for line in lines:
        textob.textLine(line)

    if item.item_image:
        image_path = item.item_image.path 
        x = page_width/2 - 60  # X-coordinate
        y = 120 # Y-coordinate
        width = 2 * inch  # Desired width
        height = 2 * inch  # Desired height
        try:
            with Image.open(image_path) as img:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                img_buffer = io.BytesIO()
                img.save(img_buffer,format="PNG")
                img_buffer.seek(0)
            c.drawImage(ImageReader(img_buffer),x,y,width,height)
        except Exception as e:
            print(f"Error adding image: {e}")
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    filename = f'{item.item_name}.pdf'
    return FileResponse(buf, as_attachment=True, filename=filename)

def update_item_quantity(request,warehouse_slug,item_id):
    if request.method == "POST":
        item = get_object_or_404(InventoryItem, id=item_id)
        quantity = request.POST.get('quantity')
        if quantity.isdigit():
            item.quantity = int(quantity)
            item.save()

    return redirect('list-item', warehouse_slug=warehouse_slug)