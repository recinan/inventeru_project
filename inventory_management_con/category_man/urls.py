from django.urls import path
from . import views

urlpatterns = [
    path('add-category', views.add_category,name='add-category'),
    path('list-warehouse/list-category/<slug:warehouse_slug>/', views.list_categories, name='list-category'),
    path('add-category-warehouse/<slug:warehouse_slug>', views.add_category_warehouse,name='add-category-warehouse'),
    path('list-allcategories',views.list_allcategories,name='list-allcategories'),
    path('get-categories-for-warehouse/<int:warehouse_id>/', views.get_categories_for_warehouse, name='get_categories_for_warehouse'),
    path('search-category/<slug:warehouse_slug>',views.search_category_bar,name='search-category'),
    path('delete-category/<slug:category_slug>',views.delete_category,name='delete-category')
]
