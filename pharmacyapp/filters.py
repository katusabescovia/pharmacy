import django_filters
from .models import *

class DivineFilter(django_filters.FilterSet):
    class Meta:
        model = Divine
        fields = ['item_name']

class ClearanceFilter(django_filters.FilterSet):
    class Meta:
        model = Clearance
        fields = ['Customers_name']
