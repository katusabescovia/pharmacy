from django.shortcuts import render
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'pharmacyapp/index.html')


def base(request):
    return render(request,'pharmacyapp/base.html')
# def index(request):
#     return render(request,'pharmacyapp/index.html')