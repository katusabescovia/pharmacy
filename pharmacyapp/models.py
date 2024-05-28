from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Divine (models.Model):
    Category_item = models.ForeignKey(Category, on_delete=models.CASCADE) 
    item_name=models.CharField(max_length=200,null=True, blank=True)
    quantity=models.IntegerField(default=0)  
    unit_price=models.IntegerField(default=0,null=True, blank=True)
    received_quantity=models.IntegerField(default=0,null=True,blank=True)
    issued_quantity=models.IntegerField(default=0,null=True,blank=True)
    date_of_stock=models.DateField(default=timezone.now)
    def __str__(self):
        return self.item_name
class Salerecord(models.Model):
    name_of_the_item=models.CharField(max_length=100,null=True,blank=True)
    payee=models.CharField(max_length=100,null=True,blank=True)
    quantity_sold=models.IntegerField(default=0,null=True,blank=True)
    amount_received=models.IntegerField(default=0,null=True,blank=True)
    date_of_sale=models.DateField(default=timezone.now)
    unit_price=models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return self.name_of_the_item
    def total_price(self):
        total_price=self.quantity_sold*self.unit_price
        return int(total_price)
    def change(self):
        change=self.total_price()-self.amount_received
        return int(change)



    
    


    

