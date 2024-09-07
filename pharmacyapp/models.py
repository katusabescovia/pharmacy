from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Divine(models.Model):
    Category_item = models.ForeignKey(Category, on_delete=models.CASCADE) 
    item_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(default=0)  
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    received_quantity = models.IntegerField(default=0, null=True, blank=True)
    issued_quantity = models.IntegerField(default=0, null=True, blank=True)
    date_of_stock = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.item_name

    def expenses(self):
        # Handle None values by defaulting to 0
        return (self.quantity or 0) * (self.unit_price or 0)
    
    @classmethod
    def total_expenses(cls):
        return sum(instance.expenses() for instance in cls.objects.all())

class Salerecord(models.Model):
    name_of_the_item = models.ForeignKey(Divine, on_delete=models.CASCADE, blank=True)
    payee = models.CharField(max_length=100, null=True, blank=True)
    quantity_sold = models.IntegerField(default=0, null=True, blank=True)
    Selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    date_of_sale = models.DateField(default=timezone.now, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    
    def __str__(self):
        return self.payee or "No payee"

    def total_price(self):
        quantity = self.quantity_sold or 0
        selling_price = self.Selling_price or 0
        return quantity * selling_price
    
    def change(self):
        return self.total_price() - (self.amount_received or 0)
    
    def profit(self):
        total_price = self.total_price()
        unit_price = self.unit_price or 0
        return total_price - (self.quantity_sold or 0) * unit_price
    
    def Clearing_debt(self):
        return self.change() - (self.amount_due or 0)
    
    @classmethod
    def total_profits(cls):
        return sum(instance.profit() for instance in cls.objects.all())
    
    @classmethod
    def total_debt(cls):
        return sum(instance.change() for instance in cls.objects.all())

class Clearance(models.Model):
    Customers_name = models.ForeignKey(Salerecord, on_delete=models.CASCADE)
    name_of_the_item = models.ForeignKey(Divine, on_delete=models.CASCADE)
    clearace_date = models.DateField(default=timezone.now)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    status = models.CharField(choices=[('complete', 'Complete'), ('pending', 'Pending')], max_length=100)
    
    def __str__(self):
        return self.Customers_name.payee if self.Customers_name else "No Customer"
