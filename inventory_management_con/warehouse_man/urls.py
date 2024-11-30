from django.urls import path
from . import views

urlpatterns = [
    path('add-warehouse',views.add_warehouse,name='add-warehouse')
]
