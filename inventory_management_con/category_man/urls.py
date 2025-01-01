from django.urls import path
from . import views

urlpatterns = [
    path('list-warehouse/list-category/<slug:warehouse_slug>/', views.list_categories, name='list-category'),
    path('add-category-warehouse/<slug:warehouse_slug>', views.add_category_warehouse,name='add-category-warehouse'),
    path('list-allcategories',views.list_allcategories,name='list-allcategories'),
    path('search-category/<slug:warehouse_slug>',views.search_category_bar,name='search-category'),
    path('delete-category/<slug:warehouse_slug>/<slug:category_slug>',views.delete_category,name='delete-category')
]
