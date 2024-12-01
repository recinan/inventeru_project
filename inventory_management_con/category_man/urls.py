from django.urls import path
from . import views

urlpatterns = [
    path('add-category', views.add_category,name='add-category'),
    path('get-categories-for-warehouse/<int:warehouse_id>/', views.get_categories_for_warehouse, name='get_categories_for_warehouse')
]
