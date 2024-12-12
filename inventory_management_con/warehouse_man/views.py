from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import WarehouseForm
from .models import Warehouse
from inventory_man.models import InventoryItem
from category_man.models import Category
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Create your views here.

@login_required(login_url='login')
def list_warehouse(request):
    warehouse_list = Warehouse.objects.filter(user = request.user.id)
    context = {
        'warehouselist':warehouse_list
    }
    return render(request, 'warehouse_man/list_warehouse.html',context)

login_required(login_url='login')
def add_warehouse(request):
    if request.method == 'POST':
        warehouse_form= WarehouseForm(request.POST, user=request.user)
        if warehouse_form.is_valid():
            warehouse = warehouse_form.save(commit=False)
            warehouse.user = request.user
            warehouse.save()
            return redirect(reverse_lazy('list-warehouse'))
    else:
        warehouse_form= WarehouseForm(user=request.user)

    context = {
        'warehouse_form':warehouse_form
    }
    return render(request, 'warehouse_man/add_warehouse.html',context)

def edit_warehouse(request,warehouse_slug):
    warehouse = get_object_or_404(Warehouse, slug = warehouse_slug)
    if request.method == 'POST':
        warehouse_form = WarehouseForm(request.POST, instance = warehouse)
        if warehouse_form.is_valid():
            warehouse = warehouse_form.save(commit=False)
            warehouse.user = request.user
            warehouse.save()
            return redirect(reverse_lazy('warehouse-detail', kwargs={'warehouse_slug':warehouse_slug}))
    else:
        warehouse_form = WarehouseForm(instance = warehouse)

    context = {
        'warehouse_form':warehouse_form
    }
    return render(request,'warehouse_man/edit_warehouse.html',context)

@login_required(login_url='login')
def warehouse_detail(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user = request.user,slug = warehouse_slug)
    categories = Category.objects.filter(user = request.user, warehouse=warehouse)
    items = InventoryItem.objects.filter(user = request.user, warehouse=warehouse)
    context = {
        'warehouse':warehouse,
        'categories':categories,
        'items':items
    }
    
    return render(request, 'warehouse_man/warehouse-detail.html',context)

def warehouse_detail_pdf(request, warehouse_slug, category_slug=None):
    warehouse = get_object_or_404(Warehouse, user = request.user,slug = warehouse_slug)
    categories = Category.objects.filter(user = request.user, warehouse=warehouse)
    items = InventoryItem.objects.filter(user = request.user, warehouse=warehouse)
    # If category slug comes as parameter
    if category_slug is not None:
        category = get_object_or_404(Category, user=request.user, slug = category_slug, warehouse=warehouse)
        items = InventoryItem.objects.filter(user=request.user, warehouse=warehouse,category=category)

    pdfmetrics.registerFont(TTFont("CourierNew","static/fonts/couriernew.ttf"))

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter,bottomup=0)

    page_width, page_height = letter

    c.setFont("Helvetica-Bold",14)
    c.drawString(80,30,f"{warehouse.warehouse_name}")
    c.setLineWidth(3)
    c.line(50,50,page_width-50,50)

    #warehouse info text object
    warehouse_info_textob = c.beginText()
    warehouse_info_textob.setTextOrigin(180, 20)
    warehouse_info_textob.setFont("Helvetica",8)
    warehouse_info_textob.textLine(f"Adress: {warehouse.neighborhood} {warehouse.street} {warehouse.district} / {warehouse.city} {warehouse.country} {warehouse.postal_code}")
    warehouse_info_textob.textLine("-----------------------------------------------------------------------------------------------------------------------------------------")
    warehouse_info_textob.textLine(f"Phone Number: {warehouse.phone_number}")
    #warehouse_info_textob.textLine(f"Total Number of Categories: {categories.count()} - Total Number of Items: {items.count()}")
    c.setLineWidth(1)
    #c.line(50,100,page_width-50,100)
    c.drawText(warehouse_info_textob)
    

    #Products info text object
    products = c.beginText()
    products.setTextOrigin(80,inch)
    products.setFont("CourierNew",10)
    table_header = ("C".ljust(5) 
                    + "Name".ljust(15) 
                    + "Qty".ljust(10) 
                    + "Price".ljust(15) 
                    + "Description".ljust(20) 
                    + "Category".ljust(20))
    products.textLine(table_header)
    products.textLine("-"*80)
    lines = []
    i = 1
    for item in items:
        line = (f"{str(i)}-".ljust(5)
        + f"{item.item_name}".ljust(15) 
        + f"{item.quantity} {item.unit}".ljust(10)
        + f"{item.price} {item.currency}".ljust(15)
        + f"{item.description[:20]}".ljust(20) 
        + f"{item.category}".ljust(20) )
        #lines.append(f"{i}- " + f"{item.item_name}".ljust(15) + f"{item.quantity}".ljust(5) + f"{item.description[:20]}".ljust(20) + f"{item.category}".ljust(20) + f"{item.warehouse}".ljust(15))
        products.textLine(line)
        i+=1

    #for line in lines:
     #   products.textLine(line)

    c.drawText(products)
    c.showPage()
    c.save()
    buf.seek(0)
    filename = f'{warehouse.warehouse_name}.pdf'
    return FileResponse(buf, as_attachment=True, filename=filename)
