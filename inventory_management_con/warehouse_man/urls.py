from django.urls import path
from . import views

urlpatterns = [
    path('list-warehouse',views.list_warehouse, name='list-warehouse'),
    path('add-warehouse',views.add_warehouse,name='add-warehouse'),
    path('delete-warehouse<slug:warehouse_slug>',views.delete_warehouse, name='delete-warehouse'),
    path('warehouse-detail/<slug:warehouse_slug>',views.warehouse_detail,name='warehouse-detail'),
    path('warehouse-detail-pdf/<slug:warehouse_slug>',views.warehouse_detail_pdf,name='warehouse-detail-pdf'),
    path('warehouse-detail-pdf/<slug:warehouse_slug>/<slug:category_slug>',views.warehouse_detail_pdf,name='warehouse-detail-pdf'),
    path('warehouse-detail/<slug:warehouse_slug>',views.category_per_warehouse_chart, name='category-per-warehouse-chart'),
    path('warehouse-detail/<slug:warehouse_slug>',views.products_per_category_chart, name='product-per-warehouse-chart')
]
