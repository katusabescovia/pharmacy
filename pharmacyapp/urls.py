from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',auth_views.LoginView.as_view(template_name ='pharmacyapp/login.html'), name = 'login'),
    # path('base/', views.base, name='base'),
    path('item/', views.item, name='item'),
    path('itemadd/', views.itemadd, name='itemadd'),
    path('add_to_stock/<int:pk>/', views.add_to_stock, name='add_to_stock'),
    path('all_sales/', views.all_sales, name='all_sales'),
    path('issue_item/<int:pk>/', views.issue_item, name='issue_item'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt_detail/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('itemdelete/<int:pk>/', views.itemdelete, name='itemdelete'),
]





