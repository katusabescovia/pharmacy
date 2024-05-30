from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.db.models import Sum


from .forms import *
from .models import *
from django.contrib.postgres.search import SearchQuery, SearchVector
from . filters import *
from django.http import HttpResponseBadRequest


# Create your views here.

def index(request):
    return render(request,'pharmacyapp/index.html')


# def base(request):
#     return render(request,'pharmacyapp/base.html')
@login_required
def item(request):
    item=Divine.objects.all().order_by('id')
    items=DivineFilter(request.GET,queryset=item)
    item=items.qs
    return render(request,'pharmacyapp/item.html',{'items':items,'item':item})
@login_required
def itemadd(request):
    if request.method == 'POST':
        form=Addnew_item(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('item')
    else:
        form=Addnew_item()    
    return render(request,'pharmacyapp/itemadd.html',{'form':form})
@login_required
def add_to_stock(request,pk):
    item=Divine.objects.get(id=pk)
    if request.method == 'POST':
        form=Addstock(request.POST)
        if form.is_valid():
           received_quantity=request.POST.get('received_quantity')  
           if received_quantity:
               try:
                   added_quantity=int(received_quantity)
                   item.quantity += added_quantity
                   item.save()
                   print(added_quantity)
                   print(item.quantity)
                   return redirect('item')
               except ValueError :
                   return HttpResponseBadRequest("Invalid quantity")
    else:
        form=Addstock()
    return render(request,'pharmacyapp/add_to_stock.html',{'form':form,'item':item})           

    
def all_sales(request):
    sales=Salerecord.objects.all()
    total=sum([items.amount_received for items in sales])
    change=sum([items.change() for items in sales])
    net=total-change
    return render(request,'pharmacyapp/all_sales.html',{'sales':sales,'total':total,'change':change,'net':net})


def issue_item(request,pk):
    item=Divine.objects.get(id=pk)
    sales_form=Sellforms(request.POST)
    if request.method == 'POST':
        if sales_form.is_valid():
            new_salerecord=sales_form.save(commit=False)
            new_salerecord.name_of_the_item=item
            new_salerecord.unit_price=item.unit_price
            new_salerecord.save()
            issued_item = int(request.POST.get('quantity_sold'))
            item.quantity -= issued_item
            item.save()
            print(item.item_name)
            print(request.POST['quantity_sold'])
            print(item.quantity)
            return redirect('receipt')
    return render(request,'pharmacyapp/issue_item.html',{'sales_form':sales_form})
def receipt(request):
    sales=Salerecord.objects.all().order_by('id')
    return render(request,'pharmacyapp/receipt.html',{"sales":sales})

def receipt_detail(request,receipt_id):
    receipt=Salerecord.objects.get(id=receipt_id)
    return render(request,'pharmacyapp/receipt_detail.html',{'receipt':receipt})

def itemdelete(request,pk):
    item =get_object_or_404(Divine, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item')  
    return render(request, 'itemdelete.html', {'item': item})   
    
   
def clearance(request):   
    itemsale=Clearance.objects.all().order_by('id')
    items=ClearanceFilter(request.GET,queryset=itemsale)
    itemsale=items.qs
    return render(request,'pharmacyapp/clearance.html',{'items':items,'itemsale':itemsale})

def clearanceadd(request):
    if request.method == 'POST':
        form=Clearanceforms(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('clearance')
    else:
        form=Clearanceforms()    
    return render(request,'pharmacyapp/clearanceadd.html',{'form':form})
def logout(request):
    auth_logout(request)
    return redirect('/')

def home(request):
    recent_customers=Salerecord.objects.all()[:3]
    count_amountpaid = Salerecord.objects.aggregate(Sum('amount_received'))
    total_amountpaid=count_amountpaid.get('amount_received__sum',0)
    total_expenses = Divine.total_expenses()
    total_debt=Salerecord.total_debt()
    
    context={'recent_customers':recent_customers,'total_amountpaid':total_amountpaid,'total_expenses':total_expenses,'total_debt':total_debt}
    return render(request,'pharmacyapp/home.html',context)


