from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.

def home(request):
    #template = loader.get_template("/HtmlFiles/HelloWorld.html")
    #return render(template)
    return HttpResponse("Home Page")
