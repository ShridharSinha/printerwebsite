from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.

#HomePage Views
def HomePage(request):
    #context = {'Quota' : '00:31:23'}
    return render(request, 'HomePage.html')


#Schedule Views
def Schedule(request):
    #return HttpResponse("Schedule")
    return render(request, 'SchedulePage.html')


#Submit Views
def Submission(request):
    #return HttpResponse("Submission")
    return render(request, 'SubmitFile.html')

def SubmissionForm(request):
    return HttpResponse("Submission Form")

def Success(request):
    return HttpResponse("Submission Success")

def Fail(request):
    return HttpResponse("Submission Fail")


#Account Views
def AccountData(request):
    #return HttpResponse("Account Data")
    return render(request, 'AccountData.html')

def EditAccount(request):
    return HttpResponse("Account Editor")

def Login(request):
    return HttpResponse("Login to Account")

def SignUp(request):
    return HttpResponse("Create an Account")
