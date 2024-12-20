from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login_user, name='login'),
    path('profil/<str:username>',views.profile_update, name='profile-update'),
    path('logout/',views.logout, name='logout')
]
