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
from django.core.exceptions import ValidationError

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
    categories = Category.objects.filter(user = request.user, warehouse=warehouse).order_by('date_created')
    items = InventoryItem.objects.filter(user = request.user, warehouse=warehouse)
    inventory_items_less_than_five= InventoryItem.objects.filter(user=request.user,warehouse=warehouse, quantity__lte = 5 )
    
    address = f"{warehouse.neighborhood} {warehouse.street} {warehouse.district}/{warehouse.city} {warehouse.country} {warehouse.postal_code}"
    m = warehouse_location(address=address)
    category_chart = category_per_warehouse_chart(request,warehouse_slug)
    product_chart,category_slug = products_per_category_chart(request,warehouse_slug)
    if request.method == "POST":
        warehouse = warehouse
        form = WarehouseForm(request.POST,user=request.user ,instance = warehouse)
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
        'category_chart':category_chart,
        'product_chart':product_chart,
        'chart_options':CHART_OPTIONS,
        'selected_category':category_slug
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
    
    if not categories:
        return empty_chart("There is no category")

    category_data = {}
    for category in categories:
        max_quantity = InventoryItem.objects.filter(user=request.user, category=category).aggregate(total=models.Sum('quantity'))['total'] or 0
        if max_quantity > 0:
            category_data[category.category_name] = max_quantity
    labels = list(category_data.keys())
    sizes = list(category_data.values())
    if not sizes:
        sizes = list()
        plt.figure(figsize=(4,4))
        plt.pie(sizes, labels=labels,autopct='%1.1f%%',startangle=140,textprops={'fontsize':10}, labeldistance=0.8)
        plt.title('Categories percentage of warehouse')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()
        return empty_chart("There is no product")
    
    plt.figure(figsize=(4,4))
    plt.pie(sizes, labels=labels,autopct='%1.1f%%',startangle=140, textprops={'fontsize':10}, labeldistance=0.8)
    plt.title('Categories percentage of warehouse')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return image_base64

def products_per_category_chart(request, warehouse_slug):
    warehouse = get_object_or_404(Warehouse, user=request.user, slug=warehouse_slug)
    category_slug = request.GET.get('selected_category')
    if not category_slug:
        category = Category.objects.filter(user=request.user,warehouse=warehouse).first()
        if not category:
            return (empty_chart("There is no product"),category_slug)
        category_slug = category.slug
    category = get_object_or_404(Category, user=request.user, warehouse=warehouse, slug=category_slug)
    inventory_items = InventoryItem.objects.filter(user=request.user, warehouse=warehouse, category=category)
    total_quantity = inventory_items.aggregate(total=models.Sum('quantity'))['total'] or 0
    item_data = {}  
    for item in inventory_items:
        if item.quantity > 0:
            item_data[item.item_name] = item.quantity
    labels = list(item_data.keys())
    sizes = list(item_data.values())
    threshold = 5
    filtered_labels = []
    percentages = []
    if total_quantity > 0:
        for size in sizes:
            percentage = (size/total_quantity)*100
            percentages.append(percentage)
        for label, percentage in zip(labels, percentages):
            if percentage >= threshold:
                filtered_labels.append(label)
            else:
                filtered_labels.append("")
    else:
        filtered_labels=[]
    if not sizes:
        sizes = list()
        plt.figure(figsize=(4,4))
        plt.pie(sizes, labels=filtered_labels, autopct='%1.1f%%',startangle=140)
        plt.title(f'Products percentage of {category.category_name}')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()
        return (empty_chart("There is no product"),category_slug)
    plt.figure(figsize=(4,4))
    plt.pie(sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=140,textprops={'fontsize':10}, labeldistance=0.8)
    plt.title(f'Products percentage of {category.category_name}')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return (image_base64,category_slug)

def empty_chart(title:str):

    fig, ax = plt.subplots(figsize=(4, 4))

    # Boş bir pie chart çiz (sadece kenar çizgisi olacak)
    ax.pie([], labels=[], wedgeprops={'linewidth': 1, 'edgecolor': 'black'})

    # İçini doldurmak için bir daire ekle
    circle = plt.Circle((0, 0), 0.7, color="#3266a8", zorder=0)  # Çember yarıçapını ve rengini ayarlayın
    ax.add_artist(circle)

    # Başlık ekle
    plt.title(title)

    # Görseli kaydet ve base64 olarak döndür
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)
    return image_base64