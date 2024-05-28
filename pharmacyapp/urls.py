from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('base',views.base,name='base'),
    path('login/',auth_views.LoginView.as_view(template_name ='pharmacyapp/login.html'), name = 'login'),
]