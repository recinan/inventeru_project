from django.urls import path
from . import views

urlpatterns = [
    path('plan-page/',views.plan_page,name='plan-page'),
    path('upgrade-plan<int:plan_id>',views.upgrade_plan,name='upgrade-plan')
]
