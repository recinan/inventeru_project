from django.urls import path
from . import views

urlpatterns = [
    path('list-warehouse',views.list_warehouse, name='list-warehouse'),
    path('add-warehouse',views.add_warehouse,name='add-warehouse'),
    path('edit-warehouse/<slug:warehouse_slug>',views.edit_warehouse,name='edit-warehouse'),
    path('warehouse-detail/<slug:warehouse_slug>',views.warehouse_detail,name='warehouse-detail'),
    path('warehouse-detail-pdf/<slug:warehouse_slug>',views.warehouse_detail_pdf,name='warehouse-detail-pdf')

]
