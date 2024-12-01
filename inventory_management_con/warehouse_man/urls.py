from django.urls import path
from . import views

urlpatterns = [
    path('list-warehouse',views.list_warehouse, name='list-warehouse'),
    path('add-warehouse',views.add_warehouse,name='add-warehouse')
]
