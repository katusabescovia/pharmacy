from django.forms import ModelForm
from . models import *
from django import forms

class Addnew_item(ModelForm):
    class Meta:
        model = Divine
        fields =['Category_item','item_name','quantity','unit_price','date_of_stock']

class Addstock(ModelForm):
    class Meta:
        model = Divine
        fields =['received_quantity']  


class Sellforms(ModelForm):
    class Meta:
        model = Salerecord 
        fields =['name_of_the_item','payee','quantity_sold','amount_received','date_of_sale']             




   