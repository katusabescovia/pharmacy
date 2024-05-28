from django.shortcuts import render
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'pharmacyapp/index.html')


def base(request):
    return render(request,'pharmacyapp/base.html')
# def index(request):
#     return render(request,'pharmacyapp/index.html')from django.shortcuts import render,redirect,get_object_or_404
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import *
from .models import *
from django.contrib.postgres.search import SearchQuery, SearchVector
from . filters import *
from django.http import HttpResponseBadRequest


# Create your views here.
@login_required
def item(request):
    item=Divine.objects.all()

    return render(request,'item.html')

def itemadd(request):
    return render(request,'itemadd.html')

def add_to_stock(request,pk):
    return render(request,'stock.html')
def all_sales(request):
    return render(request,'all_sales.html')
def issue_item(request,pk):
    return render(request,'issue_item.html')
def receipt(request):
    return render(request,'receipt.html')

def receipt_detail(request,receipt_id):
    return render(request,'receipt_detail.html')

def itemdelete(request,id):
    return render(request,'itemdelete.html')
   
    