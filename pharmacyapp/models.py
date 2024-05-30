from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Divine(models.Model):
    Category_item = models.ForeignKey('Category', on_delete=models.CASCADE) 
    item_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(default=0)  
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    received_quantity = models.IntegerField(default=0, null=True, blank=True)
    issued_quantity = models.IntegerField(default=0, null=True, blank=True)
    date_of_stock = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.item_name if self.item_name else "No Item Name"

    def expenses(self):
        return self.quantity * self.unit_price

    @classmethod
    def total_expenses(cls):
        total_expenses = 0
        for divine_instance in cls.objects.all():
            total_expenses += divine_instance.expenses()
        return total_expenses

class Salerecord(models.Model):
    name_of_the_item = models.CharField(max_length=100, null=True, blank=True)
    payee = models.CharField(max_length=100, null=True, blank=True)
    quantity_sold = models.IntegerField(default=0, null=True, blank=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    date_of_sale = models.DateField(default=timezone.now,null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
   
    
    def __str__(self):
        return self.payee
    
    def total_price(self):
        total_price = self.quantity_sold * self.unit_price
        return total_price
    
    def change(self):
        change = self.total_price() - self.amount_received
        return change
    
    @classmethod
    def total_debt(cls):
        total_debt = 0
        for salerecord_instance in cls.objects.all():
            total_debt += salerecord_instance.change()
        return total_debt
class Clearance(models.Model):
    Customers_name= models.ForeignKey(Salerecord, on_delete=models.CASCADE)
    name_of_the_item = models.CharField(max_length=100, null=True, blank=True)
    clearace_date = models.DateField(default=timezone.now)
    amount_paid=models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    status = models.CharField(choices=[('complete', 'complete'), ('Pending', 'pending')],max_length=100)
    def __str__(self):
        return self.Customers_name
