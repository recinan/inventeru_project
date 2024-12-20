from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import WarehouseForm
from .models import Warehouse
from inventory_man.models import InventoryItem
from category_man.models import Category
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import folium
import googlemaps
from decouple import config
from django.db import models
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64


matplotlib.use('Agg')

# Create your views here.

@login_required(login_url='login')
def list_warehouse(request):
    warehouse_list = Warehouse.objects.filter(user = request.user.id, is_active=True)
    context = {
        'warehouselist':warehouse_list
    }
    return render(request, 'warehouse_man/list_warehouse.html',context)

login_required(login_url='login')
def add_warehouse(request):
    user_warehouse_count = Warehouse.objects.filter(user=request.user).count()
    user_warehouse_count_limit = request.user.get_warehouse_limit()

    if user_warehouse_count >= user_warehouse_count_limit:
        messages.error(request, "You achieved your warehouse limit!")
        return redirect(reverse_lazy('list-warehouse'))

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

def warehouse_location(address):
    google_api_key = config("GOOGLE_MAPS_API")
    gmaps = googlemaps.Client(key=google_api_key)
    geocode_result = gmaps.geocode(address)
    print(geocode_result)

    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        country = geocode_result[0].get('formatted_address', "Unknown Location")
    else:
        lat, lng, country = 0, 0, "Unknown Location"

    m = folium.Map(location=[lat, lng], zoom_start=15)
    folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)
    m = m._repr_html_()
    return m
    
@login_required(login_url='login')
def warehouse_detail(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user = request.user,slug = warehouse_slug)
    categories = Category.objects.filter(user = request.user, warehouse=warehouse)
    items = InventoryItem.objects.filter(user = request.user, warehouse=warehouse)
    inventory_items_less_than_five= InventoryItem.objects.filter(user=request.user,warehouse=warehouse, quantity__lte = 5 )
    
    address = f"{warehouse.neighborhood} {warehouse.street} {warehouse.district}/{warehouse.city} {warehouse.country} {warehouse.postal_code}"
    m = warehouse_location(address=address)
    category_chart = category_per_warehouse_chart(request,warehouse_slug)

    if request.method == "POST":
        warehouse = warehouse
        form = WarehouseForm(request.POST, instance = warehouse)
        if form.is_valid():
            warehouse_form = form.save()
            messages.success(request, f"Warehouse has been updated")
            return redirect('warehouse-detail',warehouse_slug)
        for error in list(form.errors.values()):
            messages.error(request, error)
        
    if warehouse:
        form = WarehouseForm(instance=warehouse)

    CHART_OPTIONS = {
    'options1': 'Categories in warehouse',
    'options2': 'Products in warehouse'
    }
    
    context = {
        'map':m,
        'warehouse_form':form,
        'warehouse':warehouse,
        'categories':categories,
        'items':items,
        'less_items': inventory_items_less_than_five,
        'chart':category_chart,
        'chart_options':CHART_OPTIONS
    }
    
    return render(request, 'warehouse_man/warehouse-detail.html',context)

def warehouse_detail_pdf(request, warehouse_slug, category_slug=None, less_item_id=None):
    warehouse = get_object_or_404(Warehouse, user = request.user,slug = warehouse_slug)
    categories = Category.objects.filter(user = request.user, warehouse=warehouse)
    items = InventoryItem.objects.filter(user = request.user, warehouse=warehouse)
    # If category slug comes as a parameter
    if category_slug is not None:
        category = get_object_or_404(Category, user=request.user, slug = category_slug, warehouse=warehouse)
        items = InventoryItem.objects.filter(user=request.user, warehouse=warehouse,category=category)

    less_item_id = request.GET.get('less_item_id')
    if less_item_id is not None and less_item_id == 'less_items' :
        items = InventoryItem.objects.filter(user=request.user, warehouse=warehouse, quantity__lte = 5).order_by('date_created')


    pdfmetrics.registerFont(TTFont("CourierNew","static/fonts/couriernew.ttf"))

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter,bottomup=0)

    page_width, page_height = letter
    line_height = 12

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
    
    c.setLineWidth(1)
    c.drawText(warehouse_info_textob)
    
    y_position = 65
    x_position = 80

    #Products info text object
    products = c.beginText()
    products.setTextOrigin(x_position,y_position)
    products.setFont("CourierNew",10)
    table_header = ("C".ljust(5) 
                    + "Name".ljust(15) 
                    + "Qty".ljust(10) 
                    + "Price".ljust(15) 
                    + "Description".ljust(20) 
                    + "Category".ljust(20))
    products.textLine(table_header)
    y_position += line_height
    products.textLine("-"*80)
    y_position += line_height
    i = 1
    for item in items:

        if y_position >= page_height - 30:
            c.drawText(products)
            c.showPage()
            products = c.beginText()
            y_position = 20
            products.setTextOrigin(x_position,y_position)
            products.setFont("CourierNew",10)
            products.textLine(table_header)
            y_position += line_height
            products.textLine("-"*80)
            y_position += line_height

        line = (f"{str(i)}-".ljust(5)
        + f"{item.item_name}".ljust(15) 
        + f"{item.quantity} {item.unit}".ljust(10)
        + f"{item.price} {item.currency}".ljust(15)
        + f"{item.description[:20]}".ljust(20) 
        + f"{item.category}".ljust(20) )
        products.textLine(line)
        y_position += line_height
        i+=1

    c.drawText(products)
    c.save()
    buf.seek(0)
    filename = f'{warehouse.warehouse_name}.pdf'
    return FileResponse(buf, as_attachment=True, filename=filename)

def delete_warehouse(request, warehouse_slug):
    item = get_object_or_404(Warehouse,user=request.user, slug=warehouse_slug)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse_lazy('list-warehouse'))
    
    context = {
        'warehouse':item
    }
    return render(request, 'warehouse_man/delete_warehouse.html',context)

def category_per_warehouse_chart(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug=warehouse_slug)
    categories = Category.objects.filter(warehouse=warehouse)
    
    category_data = {}
    for category in categories:
        max_quantity = InventoryItem.objects.filter(user=request.user, category=category).aggregate(total=models.Sum('quantity'))['total'] or 0
        if max_quantity > 0:
            category_data[category.category_name] = max_quantity

    labels = list(category_data.keys())
    sizes = list(category_data.values())

    if not sizes:
        sizes = list()
        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels,autopct='%1.1f%%',startangle=140)
        plt.title('Categories per warehouse')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        return image_base64
    
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels,autopct='%1.1f%%',startangle=140, textprops={'fontsize':10}, labeldistance=0.8)
    plt.title('Categories per warehouse')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return image_base64

