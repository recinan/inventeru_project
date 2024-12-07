from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add-item/',views.add_item, name='add-item'),
    path('add-item-warehouse/<slug:warehouse_slug>/<slug:category_slug>',views.add_item_warehouse, name='add-item-warehouse'),
    path('list-item/<slug:warehouse_slug>/',views.list_item, name='list-item'),
    path('list-item-category/<slug:category_slug>/',views.list_item_category, name='list-item-category'),
    path('item-detail/<slug:warehouse_slug>/<slug:category_slug>/<slug:item_slug>', views.item_detail, name='item-detail'),
    path('edit-item/<int:pk>', views.edit_item, name='edit-item'),
    path('delete-item/<int:pk>', views.delete_item, name='delete-item')
]
