from django.urls import path
from .import views

urlpatterns = [

    path('item/',views.item,name='item'),
    path('itemadd/',views.itemadd,name='itemadd'),
    path('add_to_stock/<str:pk>', views.add_to_stock, name='add_to_stock'),
    path('all_sales/',views.all_sales,name='all_sales'),
    path('issue_item/<str:pk>',views.issue_item,name='issue_item'),
    path('receipt/',views.receipt,name='receipt'),
    path('receipt_detail/<int:receipt_id>',views.receipt_detail,name='receipt_detail'),
    path('itemdelete/<int:id>/',views.itemdelete,name='itemdelete'),
   
    
]