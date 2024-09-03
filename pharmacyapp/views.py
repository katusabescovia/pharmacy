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
import plotly.express as px
from plotly.offline import plot
import pandas as pd
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
from django.shortcuts import render
from .models import Divine, Salerecord


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
    total_expected=sum([items.total_price() for items in sales])
    total=sum([items.amount_received for items in sales])
    change=sum([items.change() for items in sales])
    net=total_expected-change
    
    return render(request,'pharmacyapp/all_sales.html',{'sales':sales,'total':total,'change':change,'net':net,'total_expected':total_expected})


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
# @login_required
# def home(request):
#     recent_customers=Salerecord.objects.all()[:3]
#     count_amountpaid = Salerecord.objects.aggregate(Sum('amount_received'))
#     total_amountpaid=count_amountpaid.get('amount_received__sum',0)
#     total_expenses = Divine.total_expenses()
#     total_debt=Salerecord.total_debt()
#     total_profits=Salerecord.total_profits()
#     context={'recent_customers':recent_customers,'total_amountpaid':total_amountpaid,'total_expenses':total_expenses,'total_debt':total_debt,'total_profits':total_profits}
#     return render(request,'pharmacyapp/home.html',context)

def services(request):
    return render(request,'pharmacyapp/services.html')


def itemedit(request,pk):
    item =get_object_or_404(Salerecord, id=pk)
    if request.method == 'POST':
        form=Sellforms(request.POST,instance=item)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('all_sales')
    else:
        form=Sellforms(instance=item)

    return render(request,'pharmacyapp/itemedit.html',{'form':form, 'item':item})



from django.db.models import Sum, ExpressionWrapper, DecimalField, F
from django.db.models.functions import TruncMonth
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from django.shortcuts import render

def home(request):
    # Expenses by day, aggregated by month for plotting
    expenses_data = (
        Divine.objects.annotate(
            month=TruncMonth('date_of_stock')
        )
        .values('month', 'date_of_stock')
        .annotate(
            total_expenses=Sum(
                ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField())
            )
        )
        .order_by('date_of_stock')
    )

    expenses_df = pd.DataFrame(expenses_data)
    expenses_df['date_of_stock'] = pd.to_datetime(expenses_df['date_of_stock'])
    expenses_df['month'] = pd.to_datetime(expenses_df['month'])

    # Profits by day, aggregated by month for plotting
    profits_data = (
        Salerecord.objects.annotate(
            month=TruncMonth('date_of_sale')
        )
        .values('month', 'date_of_sale')
        .annotate(
            total_sales=Sum(
                ExpressionWrapper(F('quantity_sold') * F('Selling_price'), output_field=DecimalField())
            ),
            total_cost=Sum(
                ExpressionWrapper(F('quantity_sold') * F('unit_price'), output_field=DecimalField())
            )
        )
        .annotate(
            total_profits=ExpressionWrapper(
                F('total_sales') - F('total_cost'), output_field=DecimalField()
            )
        )
        .order_by('date_of_sale')
    )

    profits_df = pd.DataFrame(profits_data)
    profits_df['date_of_sale'] = pd.to_datetime(profits_df['date_of_sale'])
    profits_df['month'] = pd.to_datetime(profits_df['month'])

    # Debts by day, aggregated by month for plotting
    debts_data = (
        Salerecord.objects.annotate(
            month=TruncMonth('date_of_sale')
        )
        .values('month', 'date_of_sale')
        .annotate(
            total_debt=Sum(
                ExpressionWrapper(F('quantity_sold') * F('Selling_price') - F('amount_received'), output_field=DecimalField())
            )
        )
        .order_by('date_of_sale')
    )

    debts_df = pd.DataFrame(debts_data)
    debts_df['date_of_sale'] = pd.to_datetime(debts_df['date_of_sale'])
    debts_df['month'] = pd.to_datetime(debts_df['month'])

    # Plotting
    fig_expenses = px.bar(
        expenses_df, 
        x='date_of_stock', 
        y='total_expenses', 
        title="Daily Expenses Aggregated by Month"
    )
    fig_profits = px.bar(
        profits_df, 
        x='date_of_sale', 
        y='total_profits', 
        title="Daily Profits Aggregated by Month"
    )
    fig_debts = px.bar(
        debts_df, 
        x='date_of_sale', 
        y='total_debt', 
        title="Daily Debts Aggregated by Month"
    )

    # Hover template
    hover_template = '%{x|%d %B %Y}: %{y}'

    fig_expenses.update_traces(hovertemplate=hover_template)
    fig_profits.update_traces(hovertemplate=hover_template)
    fig_debts.update_traces(hovertemplate=hover_template)

    # Update layouts to show full dates and correct month grouping
    fig_expenses.update_layout(
        xaxis_title='Date', 
        yaxis_title='Total Expenses',
        xaxis=dict(
            tickformat='%d %b %Y',  # Format dates on the x-axis
            tickvals=expenses_df['date_of_stock'],  # Set x-axis ticks to be the actual dates
            ticktext=[date.strftime('%d %b %Y') for date in expenses_df['date_of_stock']]  # Show full date
        )
    )
    fig_profits.update_layout(
        xaxis_title='Date', 
        yaxis_title='Total Profits',
        xaxis=dict(
            tickformat='%d %b %Y',  # Format dates on the x-axis
            tickvals=profits_df['date_of_sale'],  # Set x-axis ticks to be the actual dates
            ticktext=[date.strftime('%d %b %Y') for date in profits_df['date_of_sale']]  # Show full date
        )
    )
    fig_debts.update_layout(
        xaxis_title='Date', 
        yaxis_title='Total Debts',
        xaxis=dict(
            tickformat='%d %b %Y',  # Format dates on the x-axis
            tickvals=debts_df['date_of_sale'],  # Set x-axis ticks to be the actual dates
            ticktext=[date.strftime('%d %b %Y') for date in debts_df['date_of_sale']]  # Show full date
        )
    )

    expenses_plot = plot(fig_expenses, output_type='div')
    profits_plot = plot(fig_profits, output_type='div')
    debts_plot = plot(fig_debts, output_type='div')

    # Other context data
    recent_customers = Salerecord.objects.all()[:3]
    total_amountpaid = Salerecord.objects.aggregate(
        total_amount=Sum('amount_received')
    )['total_amount'] or 0
    total_expenses = Divine.objects.aggregate(
        total_expenses=Sum(
            ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField())
        )
    )['total_expenses'] or 0
    total_debt = Salerecord.objects.aggregate(
        total_debt=Sum(
            ExpressionWrapper(F('quantity_sold') * F('Selling_price') - F('amount_received'), output_field=DecimalField())
        )
    )['total_debt'] or 0
    total_profits = Salerecord.objects.aggregate(
        total_profits=Sum(
            ExpressionWrapper(F('quantity_sold') * F('Selling_price') - F('quantity_sold') * F('unit_price'), output_field=DecimalField())
        )
    )['total_profits'] or 0

    context = {
        'recent_customers': recent_customers,
        'total_amountpaid': total_amountpaid,
        'total_expenses': total_expenses,
        'total_debt': total_debt,
        'total_profits': total_profits,
        'expenses_plot': expenses_plot,
        'profits_plot': profits_plot,
        'debts_plot': debts_plot
    }
    return render(request, 'pharmacyapp/home.html', context)
