from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add-item/',views.add_item, name='add-item'),
    path('list-item/<slug:category_slug>/',views.list_item, name='list-item'),
    path('edit-item/<int:pk>', views.edit_item, name='edit-item'),
    path('delete-item/<int:pk>', views.delete_item, name='delete-item')
]
