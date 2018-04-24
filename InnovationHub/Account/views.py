from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def accountData(request):
    return HttpResponse("Account Information")

def editAccount(request):
    return HttpResponse("Account Editor")

def login(request):
    return HttpResponse("Account Login")

def setUp(request):
    return HttpResponse("Account Setup")
