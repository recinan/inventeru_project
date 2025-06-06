from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about',views.about, name='about_page'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add-item-warehouse/<slug:warehouse_slug>/<slug:category_slug>',views.add_item_warehouse, name='add-item-warehouse'),
    path('list-item/<slug:warehouse_slug>/',views.list_item, name='list-item'),
    path('list-item-category/<slug:warehouse_slug>/<slug:category_slug>/',views.list_item_category, name='list-item-category'),
    path('list-less-items/<slug:warehouse_slug>/',views.list_item_less_than_five, name='list-less-items'),
    path('item-detail/<slug:warehouse_slug>/<slug:category_slug>/<slug:item_slug>', views.item_detail, name='item-detail'),
    path('search-product/<slug:warehouse_slug>',views.search_product_bar,name='search-product'),
    path('item-detail-pdf/<slug:warehouse_slug>/<slug:category_slug>/<slug:item_slug>',views.item_detail_pdf,name='item-detail-pdf'),
    path('delete-item/<int:pk>/<slug:warehouse_slug>', views.delete_item, name='delete-item'),
    path('update-item-quantity/<slug:warehouse_slug>/<int:item_id>',views.update_item_quantity, name='update-item-quantity')
]
